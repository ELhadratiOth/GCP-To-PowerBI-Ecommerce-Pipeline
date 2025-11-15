#!/usr/bin/env python3
"""
Test script to verify Kaggle dataset download works
"""

import os
import sys
import time

try:
    import kagglehub
    print("✓ kagglehub imported successfully")
except ImportError as e:
    print(f"✗ Failed to import kagglehub: {e}")
    sys.exit(1)


def test_kaggle_download():
    """Test downloading the ecommerce dataset from Kaggle"""
    
    print("\n" + "="*60)
    print("Testing Kaggle Dataset Download")
    print("="*60)
    
    dataset_name = "olistbr/brazilian-ecommerce"
    
    print(f"\nDataset: {dataset_name}\n")
    
    try:
        print("Downloading dataset...")
        start_time = time.time()
        
        dataset_path = kagglehub.dataset_download(
            dataset_name,
            force_download=False  # Use cache if available
        )
        
        elapsed_time = time.time() - start_time
        print(f"✓ Download successful in {elapsed_time:.2f} seconds")
        
        # Check if directory exists and list CSV files
        if os.path.isdir(dataset_path):
            print(f"✓ Dataset path exists: {dataset_path}")
            
            csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
            print(f"✓ Found {len(csv_files)} CSV files:")
            
            for csv_file in csv_files:
                file_path = os.path.join(dataset_path, csv_file)
                file_size = os.path.getsize(file_path)
                size_mb = file_size / (1024 * 1024)
                print(f"  - {csv_file}: {size_mb:.2f} MB")
            
            print("\n" + "="*60)
            print("✓ Download test PASSED")
            print("="*60)
            return True
        else:
            print(f"✗ Dataset path does not exist: {dataset_path}")
            return False
            
    except Exception as e:
        print(f"✗ Download failed: {type(e).__name__}: {str(e)}")
        print("\n" + "="*60)
        print("✗ Download test FAILED")
        print("="*60)
        return False


if __name__ == "__main__":
    success = test_kaggle_download()
    sys.exit(0 if success else 1)
