"""
BihnCOM Subclipper Script

This script automates the process of creating subclips from all video clips in the current timeline of a DaVinci Resolve project.
It retrieves each clip's details, such as start and end frames, and creates corresponding subclips in the Media Pool.

Steps:
1. Import the necessary DaVinci Resolve scripting API.
2. Retrieve all video clips from the current timeline.
3. For each clip, creates a subclip in the active bin in the Media Pool.

Usage:
- Ensure DaVinci Resolve is running with a project and timeline loaded.
- Run this script from the DaVinci Resolve scripting console or an external Python environment configured to use the DaVinci Resolve API.
"""

# Import the Resolve API

import sys
sys.path.append('/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules')


import DaVinciResolveScript as dvr


# Get Resolve object and project manager
resolve = dvr.scriptapp("Resolve")
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
media_pool = project.GetMediaPool()

# Get the current timeline
timeline = project.GetCurrentTimeline()
print("Creating subclips from timeline'", timeline.GetName(), "'")

if not timeline:
    print("No timeline selected.")
    exit()


# Get all clips in the timeline
timeline_items = timeline.GetItemListInTrack("Video", 1)

if not timeline_items:
    print("No clips found in the timeline.")
    exit()

# Create subclips for each timeline clip
for item in timeline_items:
    # Get the source clip details
    media_pool_item = item.GetMediaPoolItem()
    start_frame = item.GetStart()
    end_frame = item.GetEnd()
    source_start_frame = item.GetSourceStartFrame()
    source_end_frame = item.GetSourceEndFrame()

    if media_pool_item:
        # Create a subclip in the Media Pool
        clip_name = media_pool_item.GetName()
        file_path = media_pool_item.GetClipProperty("File Path")

        print(f"Processing clip: {clip_name}")
        print(f"File Path: {file_path}")

        print(f"Source Start Frame: {source_start_frame}, Source End Frame: {source_end_frame}")

        # Add subclip to Media Pool:
        subClip = {
            "media" : file_path,
            "startFrame": int(source_start_frame),
            "endFrame": int(source_end_frame),
        }

        print("\n")

        resolve.GetMediaStorage().AddItemListToMediaPool([ subClip ])



print("All subclips created successfully!")

# End of script