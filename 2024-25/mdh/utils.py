import numpy as np

def euclidean_distance(vector1, vector2):
    """
    Calculate the Euclidean distance between two numpy vectors.
    
    Parameters:
    -----------
    vector1 : numpy.ndarray
        First vector
    vector2 : numpy.ndarray
        Second vector
    
    Returns:
    --------
    float
        Euclidean distance between the two vectors
    
    Formula:
    --------
    d = sqrt(sum((x_i - y_i)^2))
    """
    return np.sqrt(np.sum((vector1 - vector2) ** 2))

def cosine_distance(vector1, vector2):
    """
    Calculate the cosine distance between two numpy vectors.
    
    Parameters:
    -----------
    vector1 : numpy.ndarray
        First vector
    vector2 : numpy.ndarray
        Second vector
    
    Returns:
    --------
    float
        Cosine distance between the two vectors (1 - cosine similarity)
    
    Formula:
    --------
    cosine_similarity = (A · B) / (||A|| * ||B||)
    cosine_distance = 1 - cosine_similarity
    """
    # Calculate dot product
    dot_product = np.dot(vector1, vector2)
    
    # Calculate norms (magnitudes)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    
    # Handle zero vectors case
    if norm1 == 0 or norm2 == 0:
        return 1.0  # Maximum distance for zero vectors
    
    # Calculate cosine similarity
    cosine_similarity = dot_product / (norm1 * norm2)
    
    # Convert to distance (1 - similarity)
    return 1 - cosine_similarity