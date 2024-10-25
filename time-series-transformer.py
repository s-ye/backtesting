import torch
import torch.nn as nn
import staticvariables as sv
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import yfinance as yf
seq_length = 30

class TimeSeriesTransformer(nn.Module):
    def __init__(self, input_dim, embed_dim, num_heads, hidden_dim, num_layers, dropout=0.1):
        super(TimeSeriesTransformer, self).__init__()
        
        self.input_embedding = nn.Linear(input_dim, embed_dim)
        self.positional_encoding = self._generate_positional_encoding(embed_dim, max_len=seq_length)
        
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, dim_feedforward=hidden_dim, dropout=dropout)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        self.fc_out = nn.Linear(embed_dim, 1)
        
    def forward(self, x):
        x = self.input_embedding(x) + self.positional_encoding[:, :x.size(1), :]
        x = self.transformer_encoder(x)
        output = self.fc_out(x[:, -1, :])
        return output
    
    def _generate_positional_encoding(self, embed_dim, max_len):
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, embed_dim, 2) * -(np.log(10000.0) / embed_dim))
        pe = torch.zeros(max_len, embed_dim)
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        return pe

def create_sequences(data, seq_length):
    sequences = []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i+seq_length])
    return np.array(sequences)

def prepare_data():
    data = yf.Ticker('NVDA').history(period='5y', interval='1d')
    data = sv.processHist(data)
    features = ['Close', 'Volume', 'SMA_50', 'SMA_200', 'RSI']
    scaler = StandardScaler()
    data[features] = scaler.fit_transform(data[features])
    values = data[features].values


    values_normalized = scaler.fit_transform(values.reshape(-1, 1))

    
    sequences = create_sequences(values_normalized, seq_length)
    X = sequences[:, :-1]
    y = sequences[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_test = torch.tensor(y_test, dtype=torch.float32)

    return X_train, X_test, y_train, y_test, scaler

def train_and_save_model(X_train, y_train, input_dim, embed_dim, num_heads, hidden_dim, num_layers, num_epochs, learning_rate, save_path):
    model = TimeSeriesTransformer(input_dim, embed_dim, num_heads, hidden_dim, num_layers)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        model.train()
        optimizer.zero_grad()
        
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    torch.save(model.state_dict(), save_path)
    print(f'Model saved to {save_path}')

def load_and_evaluate_model(X_test, y_test, input_dim, embed_dim, num_heads, hidden_dim, num_layers, load_path, scaler):
    model = TimeSeriesTransformer(input_dim, embed_dim, num_heads, hidden_dim, num_layers)
    model.load_state_dict(torch.load(load_path))
    model.eval()

    with torch.no_grad():
        predictions = model(X_test)
        criterion = nn.MSELoss()
        test_loss = criterion(predictions, y_test)
        print(f'Test Loss: {test_loss.item():.4f}')

    predictions_inverted = scaler.inverse_transform(predictions.numpy().reshape(-1, 1))
    y_test_inverted = scaler.inverse_transform(y_test.numpy().reshape(-1, 1))

    plt.figure(figsize=(14, 7))
    plt.plot(predictions_inverted, label='Predictions')
    plt.plot(y_test_inverted, label='Actual')
    plt.legend()
    plt.savefig('predictions.png')
    print('Predictions plot saved as predictions.png')

if __name__ == "__main__":
    X_train, X_test, y_train, y_test, scaler = prepare_data()
    input_dim = X_train.shape[2]
    embed_dim = 64
    num_heads = 4
    hidden_dim = 128
    num_layers = 2
    num_epochs = 50
    learning_rate = 1e-5
    save_path = 'model.pth'

    train_and_save_model(X_train, y_train, input_dim, embed_dim, num_heads, hidden_dim, num_layers, num_epochs, learning_rate, save_path)
    load_and_evaluate_model(X_test, y_test, input_dim, embed_dim, num_heads, hidden_dim, num_layers, save_path, scaler)
