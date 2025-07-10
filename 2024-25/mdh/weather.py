import json
import random
import numpy as np

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

# Vocabolario meteorologico esteso
weather_vocab = {
    # Stopwords (molto comuni, presenti in quasi tutti i documenti)
    'stopwords': ['tempo', 'giorno', 'oggi', 'ieri', 'clima'],
    
    # Condizioni di base
    'conditions': ['sole', 'pioggia', 'nuvole', 'sereno', 'coperto'],
    
    # Intensità
    'intensity': ['forte', 'leggero', 'intenso', 'debole'],
    
    # Fenomeni specifici
    'phenomena': ['temporale', 'grandine', 'neve', 'nebbia', 'vento', 'umido'],
    
    # Temperature
    'temperature': ['caldo', 'freddo', 'fresco', 'tiepido']
}

def generate_weather_document(doc_id, min_length=8, max_length=25):
    """
    Generate a single weather document with realistic patterns
    """
    length = random.randint(min_length, max_length)
    document = []
    
    # Ensure stopwords are present (high probability)
    stopword_count = random.randint(2, 4)
    for _ in range(stopword_count):
        document.append(random.choice(weather_vocab['stopwords']))
    
    # Add main weather conditions
    condition_count = random.randint(3, 8)
    for _ in range(condition_count):
        document.append(random.choice(weather_vocab['conditions']))
    
    # Add remaining words from other categories
    remaining_length = length - len(document)
    all_other_words = (weather_vocab['intensity'] + 
                      weather_vocab['phenomena'] + 
                      weather_vocab['temperature'])
    
    for _ in range(remaining_length):
        if random.random() < 0.3:  # 30% chance of stopword
            document.append(random.choice(weather_vocab['stopwords']))
        else:
            document.append(random.choice(all_other_words))
    
    # Shuffle to make it more natural
    random.shuffle(document)
    
    return {
        'id': f'doc_{doc_id:03d}',
        'text': ' '.join(document),
        'length': len(document),
        'tokens': document
    }

def create_weather_patterns():
    """
    Create documents with specific weather patterns for variety
    """
    patterns = {
        'sunny_days': {
            'conditions': ['sole', 'sereno'],
            'temperature': ['caldo', 'tiepido'],
            'weight': 0.4
        },
        'rainy_days': {
            'conditions': ['pioggia', 'coperto', 'nuvole'],
            'phenomena': ['temporale', 'umido'],
            'weight': 0.3
        },
        'winter_days': {
            'conditions': ['coperto', 'nuvole'],
            'phenomena': ['neve', 'nebbia', 'vento'],
            'temperature': ['freddo', 'fresco'],
            'weight': 0.2
        },
        'stormy_days': {
            'conditions': ['temporale', 'pioggia'],
            'phenomena': ['grandine', 'vento'],
            'intensity': ['forte', 'intenso'],
            'weight': 0.1
        }
    }
    return patterns

def generate_pattern_document(doc_id, pattern_type, pattern_config):
    """
    Generate a document following a specific weather pattern
    """
    length = random.randint(10, 20)
    document = []
    
    # Add stopwords (always present)
    stopword_count = random.randint(2, 3)
    for _ in range(stopword_count):
        document.append(random.choice(weather_vocab['stopwords']))
    
    # Add pattern-specific words
    for category, words in pattern_config.items():
        if category != 'weight':
            count = random.randint(1, 3)
            for _ in range(count):
                document.append(random.choice(words))
    
    # Fill remaining length
    remaining = length - len(document)
    all_words = []
    for category in weather_vocab.values():
        if isinstance(category, list):
            all_words.extend(category)
    
    for _ in range(remaining):
        document.append(random.choice(all_words))
    
    random.shuffle(document)
    
    return {
        'id': f'doc_{doc_id:03d}',
        'text': ' '.join(document),
        'length': len(document),
        'tokens': document,
        'pattern': pattern_type
    }

# Generate the complete dataset
dataset = []
patterns = create_weather_patterns()

# Generate 60% pattern-based documents
pattern_docs = 60
doc_counter = 1

for pattern_name, config in patterns.items():
    num_docs = int(pattern_docs * config['weight'])
    for _ in range(num_docs):
        doc = generate_pattern_document(doc_counter, pattern_name, config)
        dataset.append(doc)
        doc_counter += 1

# Generate 40% random documents
random_docs = 40
for _ in range(random_docs):
    doc = generate_weather_document(doc_counter)
    doc['pattern'] = 'random'
    dataset.append(doc)
    doc_counter += 1

# Shuffle the final dataset
random.shuffle(dataset)

# Re-assign sequential IDs
for i, doc in enumerate(dataset, 1):
    doc['id'] = f'doc_{i:03d}'

# Create vocabulary statistics
def compute_vocabulary_stats(dataset):
    """
    Compute statistics about the vocabulary
    """
    all_tokens = []
    for doc in dataset:
        all_tokens.extend(doc['tokens'])
    
    from collections import Counter
    token_counts = Counter(all_tokens)
    
    vocabulary_stats = {
        'total_documents': len(dataset),
        'total_tokens': len(all_tokens),
        'unique_tokens': len(token_counts),
        'vocabulary': dict(token_counts),
        'most_common_tokens': token_counts.most_common(10),
        'stopwords_frequency': {word: token_counts[word] for word in weather_vocab['stopwords']}
    }
    
    return vocabulary_stats

# Compute statistics
vocab_stats = compute_vocabulary_stats(dataset)

# Prepare final JSON structure
final_dataset = {
    'metadata': {
        'description': 'Extended weather conditions dataset with stopwords',
        'total_documents': len(dataset),
        'vocabulary_size': vocab_stats['unique_tokens'],
        'total_tokens': vocab_stats['total_tokens'],
        'language': 'italian',
        'domain': 'meteorology'
    },
    'vocabulary': {
        'categories': weather_vocab,
        'statistics': vocab_stats
    },
    'documents': dataset
}

# Convert to JSON
json_output = json.dumps(final_dataset, ensure_ascii=False, indent=2)

print("=== DATASET GENERATO ===")
print(f"Numero documenti: {len(dataset)}")
print(f"Vocabolario: {vocab_stats['unique_tokens']} parole uniche")
print(f"Token totali: {vocab_stats['total_tokens']}")
print()

print("=== STOPWORDS PIÙ FREQUENTI ===")
for word, freq in vocab_stats['stopwords_frequency'].items():
    print(f"{word}: {freq} occorrenze")
print()

print("=== PRIMI 5 DOCUMENTI ===")
for i in range(5):
    doc = dataset[i]
    print(f"{doc['id']}: \"{doc['text']}\" (pattern: {doc['pattern']})")
print()

print("=== TOKEN PIÙ COMUNI ===")
for token, freq in vocab_stats['most_common_tokens']:
    print(f"{token}: {freq}")

# Save to file (optional)
with open('weather_dataset.json', 'w', encoding='utf-8') as f:
    f.write(json_output)

print("\n✓ Dataset salvato in 'weather_dataset.json'")
print(f"\n=== SAMPLE JSON OUTPUT ===")
print(json_output[:1000] + "..." if len(json_output) > 1000 else json_output)