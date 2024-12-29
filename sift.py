import os
import cv2
import numpy as np
import sys

def main():
    # Load the images
    large = sys.argv[1]
    query = sys.argv[2]
    london_image = cv2.imread(large, cv2.IMREAD_GRAYSCALE)
    query_image = cv2.imread(query, cv2.IMREAD_GRAYSCALE)

    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Find the keypoints and descriptors with SIFT
    keypoints_london, descriptors_london = sift.detectAndCompute(london_image, None)
    keypoints_query, descriptors_query = sift.detectAndCompute(query_image, None)

    # Create a KNN matcher object
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)

    # Match descriptors using KNN
    matches = bf.knnMatch(descriptors_query, descriptors_london, k=2)

    # Apply ratio test to filter good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:  # Lowe's ratio test
            good_matches.append(m)

    # Draw the good matches
    matched_image = cv2.drawMatches(query_image, keypoints_query, london_image, keypoints_london, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Show the matched image
    #cv2.imshow('Matches', matched_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    print(large, query, len(good_matches))

    # Optionally, calculate the homography if enough good matches are found
    if len(good_matches) > 50:  # Ensure enough matches are found
        src_pts = np.float32([keypoints_query[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints_london[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Find homography
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # Get the dimensions of the query image
        h, w = query_image.shape

        # Define the corners of the query image
        query_corners = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

        # Project the corners to the larger image
        if M is not None:
            dst_corners = cv2.perspectiveTransform(query_corners, M)

            # Draw the polygon on the larger image
            london_image_color = cv2.cvtColor(london_image, cv2.COLOR_GRAY2BGR)
            cv2.polylines(london_image_color, [np.int32(dst_corners)], isClosed=True, color=(0, 255, 0), thickness=3)

            # Show the result
            #cv2.imshow('Detected Query Image', london_image_color)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            filename = os.path.join("result", os.path.basename(large) + "-" + os.path.basename(query))
            print(f"writing {filename}")
            cv2.imwrite(filename, london_image_color)

    else:
        print("Not enough good matches found.")

if __name__=="__main__":
    main()
