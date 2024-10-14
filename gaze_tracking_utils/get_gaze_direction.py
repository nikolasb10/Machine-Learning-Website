import torch
from PIL import Image
import torchvision.transforms as transforms

def spherical2cartesial(x):
    output = torch.zeros(x.size(0),3)
    output[:,2] = -torch.cos(x[:,1])*torch.cos(x[:,0])
    output[:,0] = torch.cos(x[:,1])*torch.sin(x[:,0])
    output[:,1] = torch.sin(x[:,1])
    return output

def get_gaze_direction(model, number_of_humans):
    image_normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

    output_gazes = []
    # Create the model input
    for human in range(number_of_humans):
        model_input = torch.zeros(7,3,224,224)
        image_folder = f"human_{human}"
        for count in range(7):
            # current_frame            = start_frame + count
            # image_path               = f"{dataset_path}/cropped_child_frames/{video_name}/{current_frame}.jpg"
            new_im                   = Image.open(f"./gaze_tracking_utils/video_frames/{image_folder}/frame_{count}.jpg")
            model_input[count,:,:,:] = image_normalize(transforms.ToTensor()(transforms.Resize((224,224))(new_im)))
        # print(model_input.size())
        output_gaze,_,_,_ = model(model_input.view(1,7,3,224,224))
        gaze = spherical2cartesial(output_gaze).detach().numpy()
        output_gazes.append(gaze)

    return output_gazes