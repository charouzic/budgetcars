from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from app.models.car import Car


def content_filtering(target_car: Car, all_cars: List[Car]) -> List[Car]:
    # Convert target car features into a text description
    target_car_text = f"{target_car.make} {target_car.price} {target_car.year} {target_car.kilometers} {target_car.fuel_type} {target_car.transmission} {target_car.color} {target_car.seats}"

    # Create a list of text features for all cars
    all_car_texts = [f"{car.make} {car.price} {car.year} {car.kilometers} {car.fuel_type} {car.transmission} {car.color} {car.seats}" for car in all_cars]

    # Use TF-IDF vectorization to convert the text features into numerical representations
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([target_car_text] + all_car_texts)

    # Compute the cosine similarity between the target car and all other cars
    cosine_similarities = linear_kernel(tfidf_matrix[0:1], tfidf_matrix).flatten()

    # Sort the cars based on their similarity score in descending order
    similar_car_indices = cosine_similarities.argsort()[::-1][1:]  # Exclude the target car itself
    similar_cars = [all_cars[index] for index in similar_car_indices]

    return similar_cars