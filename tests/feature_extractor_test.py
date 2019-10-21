from feature_extractor import Extractor

input = ["Test sentences", "How do we handle punctuation?", "What do we do about special characters", "",
        "What about empty test"]
extractor = Extractor(input)
print("input sentences:")
print(input)
print("")
vocab = extractor.get_features(7)
print("vocab:")
print(vocab)
print("")
encoded_data = extractor.encode_data_with_features(vocab)
print("encoded data:")
print(encoded_data)