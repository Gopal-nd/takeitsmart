import streamlit as st
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# -----------------------------------------------------
# 1. Embedded Text Corpus & Vocabulary Builder
# -----------------------------------------------------
TEXT_CORPUS = """
Artificial intelligence is the simulation of human intelligence processes by machines, especially computer systems. 
Specific applications of AI include expert systems, natural language processing, speech recognition and machine vision. 
Machine learning is a subset of artificial intelligence that involves the use of algorithms and statistical models 
to enable computers to improve their performance on a specific task through experience. Deep learning is a subset of 
machine learning that uses multi-layered artificial neural networks to deliver state-of-the-art accuracy in tasks 
such as object detection, speech recognition, language translation and others. Data science is an interdisciplinary 
field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from structured 
and unstructured data. Data science is related to data mining, machine learning and big data.
"""

def build_vocab(corpus_text):
    words = corpus_text.lower().replace(".", "").replace(",", "").split()
    unique_words = list(set(words))
    
    # 0 is reserved for padding
    word2idx = {w: i+1 for i, w in enumerate(unique_words)}
    word2idx["<PAD>"] = 0
    idx2word = {i: w for w, i in word2idx.items()}
    
    return word2idx, idx2word

# -----------------------------------------------------
# 2. PyTorch LSTM Model
# -----------------------------------------------------
class NextWordLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim=64, hidden_dim=100):
        super(NextWordLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)
        
    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (h_n, c_n) = self.lstm(embedded)
        # Get the output of the last time step
        last_out = lstm_out[:, -1, :] 
        out = self.fc(last_out)
        return out

# -----------------------------------------------------
# 3. Model Training (Cached)
# -----------------------------------------------------
@st.cache_resource(show_spinner=False)
def train_pytorch_model():
    word2idx, idx2word = build_vocab(TEXT_CORPUS)
    vocab_size = len(word2idx)
    
    sentences = TEXT_CORPUS.lower().replace(".", "").replace(",", "").split("\n")
    sentences = [s.split() for s in sentences if len(s.split()) > 1]
    
    input_sequences = []
    for sentence in sentences:
        seq = [word2idx[w] for w in sentence]
        for i in range(1, len(seq)):
            n_gram_seq = seq[:i+1]
            input_sequences.append(n_gram_seq)
            
    max_sequence_len = max([len(x) for x in input_sequences])
    
    # Pad sequences with <PAD> (0) at the beginning
    padded_seqs = []
    for seq in input_sequences:
        pad_len = max_sequence_len - len(seq)
        padded_seqs.append([0]*pad_len + seq)
        
    padded_seqs = torch.tensor(padded_seqs, dtype=torch.long)
    
    X = padded_seqs[:, :-1]
    y = padded_seqs[:, -1]
    
    model = NextWordLSTM(vocab_size=vocab_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    # Train for a few epochs
    model.train()
    for epoch in range(100):
        optimizer.zero_grad()
        output = model(X)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()
        
    model.eval()
    return model, word2idx, idx2word, max_sequence_len

# -----------------------------------------------------
# 4. Streamlit Frontend interface
# -----------------------------------------------------
def main():
    st.set_page_config(page_title="Next Word Predictor", page_icon="🧠", layout="centered")
    st.title("🧠 Next Word Prediction (PyTorch)")
    
    st.markdown("""
        This app uses **PyTorch** to build and train an LSTM sequence model. 
        It learns from a small embedded corpus about Artificial Intelligence.
        Using PyTorch natively ensures maximum compatibility!
    """)
    
    with st.spinner("Training PyTorch LSTM on embedded corpus... please wait a moment."):
        model, word2idx, idx2word, max_seq_len = train_pytorch_model()
    
    with st.expander("Show the training corpus"):
        st.write(TEXT_CORPUS)
        
    st.subheader("Try it out!")
    input_text = st.text_input("Type a phrase (e.g. 'Artificial intelligence is'):")

    if input_text:
        words = input_text.lower().replace(".", "").replace(",", "").split()
        
        # Tokenize unknown words as <PAD> (0)
        seq = [word2idx.get(w, 0) for w in words]
        
        if len(seq) == 0:
            st.warning("Please type a word!")
            return
            
        pad_len = (max_seq_len - 1) - len(seq)
        if pad_len > 0:
            seq = [0]*pad_len + seq
        else:
            seq = seq[- (max_seq_len - 1):] # Truncate if too long
            
        X_test = torch.tensor([seq], dtype=torch.long)
        
        with torch.no_grad():
            output = model(X_test)
            probs = torch.softmax(output, dim=1)
            predicted_idx = torch.argmax(probs, dim=1).item()
            
        output_word = idx2word.get(predicted_idx, "<UNKNOWN>")
        
        st.success(f"**Predicted Next Word:** {output_word}")
        st.markdown(f"**Full sequence looks like:** {input_text} **`{output_word}`**")

if __name__ == "__main__":
    main()
