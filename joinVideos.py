import subprocess
from os import listdir, remove
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip



def convert_avi_to_mp4(avi_file_path):
    mp4_file_path = avi_file_path.replace(".avi", ".mp4")
    command = [
            "ffmpeg", "-i", avi_file_path, "-c:v", "copy", "-c:a", "copy", "-y", mp4_file_path
        ]
    subprocess.run(command, check=True) 
    return mp4_file_path

def process_video_files_in_batches(file_list, batch_size):
    all_clips = []
    temp_files_names = []
    for i in range(0, len(file_list), batch_size):
        batch = file_list[i:i+batch_size]  # Select the current batch
        clips = [VideoFileClip(file) for file in batch]

        # Concatenate the current batch
        temp_clip = concatenate_videoclips(clips)
        temp_file_name = f"temp_{i}.mp4"
        temp_clip.write_videofile(temp_file_name, codec="libx264")  # Save the temporary batch file
        temp_clip.close()
        all_clips.append(VideoFileClip(temp_file_name))
        temp_files_names.append(temp_file_name)
        
        # Close the clips after processing the batch
        for clip in clips:
            clip.close()
        
    return all_clips, temp_files_names

def cleanup(mp4_files, temp_files):
    for file in mp4_files:
        remove(file)
    for file in temp_files:
        remove(file)
    print("Cleanup succesful.")

input("This code will combine all avi files in name order in the selected directory into one mp4 file. Output will overwrite the file if it already exists!!")
toWrite = []
directory = input("Insert sources directory: ") #"/home/tony/Downloads/a9-v720-master/live/"
print("Batch size will depend on the amunt of total videos to combine and available resources. It is the amount of files being processed at the same time")
batch_size = int(input("Insert batch size: "))
output_file_name = input("Insert output file name (without extension): ")
file_list = [file_name for file_name in listdir(directory) if ".avi" in file_name]  # List AVI files in directory

for file in file_list:      #   Convert all files to mp4 and store new names in toWrite
    aviFilePath = directory + file
    mp4FilePath = convert_avi_to_mp4(aviFilePath)
    toWrite.append(mp4FilePath)


clips, temp_clips_names = process_video_files_in_batches(toWrite, batch_size)
finalClip = concatenate_videoclips(clips)
finalClip.write_videofile(f"{output_file_name}.mp4", codec="libx264")
finalClip.close()
cleanup(toWrite, temp_clips_names)