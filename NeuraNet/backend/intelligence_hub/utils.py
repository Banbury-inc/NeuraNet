from collections import Counter

class Utils:

    def f1_score(prediction, ground_truth):
        # Tokenize the strings by splitting on whitespace
        prediction_tokens = prediction.split()
        ground_truth_tokens = ground_truth.split()
        
        # Create counters to count occurrences of each token
        prediction_counter = Counter(prediction_tokens)
        ground_truth_counter = Counter(ground_truth_tokens)
        
        # Calculate the number of common tokens between prediction and ground truth
        common_tokens = prediction_counter & ground_truth_counter
        num_common_tokens = sum(common_tokens.values())
        
        # If there are no common tokens, return 0
        if num_common_tokens == 0:
            return 0.0

        # Calculate precision and recall
        precision = num_common_tokens / len(prediction_tokens)
        recall = num_common_tokens / len(ground_truth_tokens)
        
        # Calculate F1 score
        f1 = 2 * (precision * recall) / (precision + recall)
        
        return f1


