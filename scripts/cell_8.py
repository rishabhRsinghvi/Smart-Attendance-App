# Cell 8: Define function to plot predicted images
def plot_predicted_images(image_list, names, folder_path):
    unique_faces = {}
    for image_name, predicted_label in zip(image_list, names):
        if predicted_label not in unique_faces:  # Add only unique names
            unique_faces[predicted_label] = image_name
    num_images = len(unique_faces)
    fig, axes = plt.subplots(num_images, 2, figsize=(5, 5*num_images))
    for i, (predicted_label, image_name) in enumerate(unique_faces.items()):
        img_path = os.path.join(folder_path, image_name)
        img = mpimg.imread(img_path)
        axes[i, 0].imshow(img)
        axes[i, 0].axis('off')
        axes[i, 1].text(0.5, 0.5, predicted_label, fontsize=20, ha='center', va='center')
        axes[i, 1].axis('off')
    plt.tight_layout()  # Adjust spacing between subplots
    plt.show()

# Example usage
image_list = os.listdir('uploads/faces')
folder_path = 'uploads/faces'
plot_predicted_images(image_list, names, folder_path)
