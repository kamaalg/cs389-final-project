# Song Recommendation Engine
![Music Animation](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdml4MnF5dG9kdTZ6YWlqaWhiN3BoMTU2cDJ5dmVkdWVncGdnZmIzMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tqfS3mgQU28ko/giphy.gif)
---
## Overview

**Song Recommendation Engine** is an innovative project that leverages neural networks to create personalized song recommendations. The system is designed to learn user preferences from a custom dataset by mapping song embeddings to user feedback. Here's how it works:

1. **Training on Custom Dataset**:  
   The neural network is pre-trained on a custom dataset to understand song embeddings and their relationships to user preferences.

2. **Few-Shot Learning for Personalization**:  
   For each new user, the program performs a few-shot learning process:
   - The user provides feedback on 5 songs they like and 5 songs they dislike.
   - The pre-trained model is fine-tuned using these preferences to better understand the user’s taste.

3. **Personalized Recommendations**:  
   - The model generates a sigmoid score to predict the likelihood of the user enjoying a given song.
   - Songs with embeddings similar to the user’s 5 liked songs are presented to the model.
   - If the model predicts the user will like a song, it outputs a score of `1`.

This dynamic process ensures that the recommendation engine adapts to individual preferences, offering tailored song suggestions based on user feedback.

## Project Structure
```
├── src/           # Source code in .ipynb format
├── data/          # Storage of all the custom datasets and temporary json files
├── embeddings     # Directory of all the saved vector embeddings
├── utils          # Folder of all auxiliary sources
├── README.md      # Project documentation
