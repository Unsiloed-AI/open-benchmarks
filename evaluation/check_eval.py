import json

def read_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def get_top_k(data: dict, k: int = None) -> dict:
    """
    Sort the scores and corresponding image_ids in descending order,
    filter out zero scores, and calculate statistics.
    If k is specified, return only the top k non-zero items.
    """
    # Create pairs of (score, image_id)
    paired_data = list(zip(data['scores'], data['image_ids']))
    
    # Sort pairs in descending order by score
    sorted_pairs = sorted(paired_data, key=lambda x: x[0], reverse=True)
    
    # Filter out pairs with a score of 0
    filtered_pairs = [pair for pair in sorted_pairs if pair[0] > 0]
    
    # Unzip the filtered pairs
    filtered_scores, filtered_image_ids = zip(*filtered_pairs) if filtered_pairs else ([], [])
    
    # If k is specified, slice the filtered data
    if k is not None and k < len(filtered_scores):
        final_scores = filtered_scores[:k]
        final_image_ids = filtered_image_ids[:k]
    else:
        final_scores = filtered_scores
        final_image_ids = filtered_image_ids
    
    # Create a new dictionary with filtered and sorted data
    result = {
        'model': data['model'],
        'scores': list(final_scores),
        'image_ids': list(final_image_ids),
        'count': len(final_scores), # Count of non-zero scores
        'success_count': len(final_scores), # All remaining scores are > 0
        'avg_similarity': sum(final_scores) / len(final_scores) if final_scores else 0
    }
    
    return result

def main():
    # Read the results file
    results = read_json('evaluation/_predicted/unsiloedvl_results.json')
    
    # Sort and filter the data (removes zero scores)
    sorted_results = get_top_k(results)
    
    # Print or save the sorted results
    print(f"Top images by score for model: {sorted_results['model']}")
    for i, (score, img_id) in enumerate(zip(sorted_results['scores'], sorted_results['image_ids'])):
        print(f"{i+1}. Score: {score:.4f}, Image: {img_id}")
    
    print(f"\nOverall average similarity (non-zero scores): {sorted_results['avg_similarity']:.4f}")
    print(f"Success count: {sorted_results['success_count']} out of {sorted_results['count']}")

    # Calculate and print average scores for top K
    print("\nAverage scores for top K:")
    scores = sorted_results['scores']
    top_k_values = [3, 5, 8, 10]

    for k in top_k_values:
        if len(scores) >= k:
            avg_top_k = sum(scores[:k]) / k
            print(f"  Top {k}: {avg_top_k:.4f}")
        else:
            print(f"  Top {k}: Not enough scores available (need {k}, have {len(scores)})")

if __name__ == "__main__":
    main()