import pyaudio as pa

STEP_LIST =        [0.01,0.01]
WINDOW_SIZE_LIST = [0.31,0.15]

STEP = 0.01 
WINDOW_SIZE = 0.31
CHANNELS = 1 
RATE = 16000
FRAME_LEN = STEP
THRESHOLD = 0.5

CHUNK_SIZE = int(STEP * RATE)

p = pa.PyAudio()
print('Available audio input devices:')
input_devices = []
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if dev.get('maxInputChannels'):
        input_devices.append(i)
        print(i, dev.get('name'))

if len(input_devices):
    dev_idx = -2
    while dev_idx not in input_devices:
        print('Please type input device ID:')
        dev_idx = int(input())
        
        
        
        
        
# cmd = b'''
# set question to display dialog ("Find Safari tab whose name includes:") default answer ""
# set searchpat to text returned of question

# tell application "Safari"
#     --
#     -- *** Step 1. get a list of all tabs that match "searchpat" ***
#     set winlist to every window
#     set winmatchlist to {}
#     set tabmatchlist to {}
#     set tabnamematchlist to {}
#     repeat with win in winlist
#         if (count of tabs of win) is not equal to 0 then 
#             set tablist to every tab of win
#             repeat with t in tablist
#                 if (searchpat is in (name of t as string)) or (searchpat is in (URL of t as string)) then
#                     set end of winmatchlist to win
#                     set end of tabmatchlist to t
#                     set end of tabnamematchlist to (id of win as string) & "." & (index of t as string) & ".  " & (name of t as string)
#                 end if
#             end repeat
            
#         end if
#     end repeat
#     --
#     -- *** Step 2. open the desired matching tab ***
#     if (count of tabmatchlist) = 1 then
#         set whichtab to (item 1 of tabnamematchlist)
#         my openTab(whichtab)
#     else if (count of tabmatchlist) = 0 then
#         display notification "No matches"
#     else
#         set whichtab to choose from list of tabnamematchlist with prompt "The following tabs match, please select one:"
#         if whichtab is not equal to false then
#             my openTab(whichtab)
#         end if
#     end if
# end tell

# on openTab(whichtab)
#     tell application "Safari"
#         set AppleScript's text item delimiters to "."
#         set tmp to text items of (whichtab as string)
#         set w to (item 1 of tmp) as integer
#         set t to (item 2 of tmp) as integer
#         set current tab of window id w to tab t of window id w
#         set index of window id w to 1
#         -- this code is an essential work-around to activate a specific window ID in Mojave
#         tell window id w
#             set visible to false
#             set visible to true
#         end tell
#     end tell
# end openTab'''
# cmd = '''tell application "Reminders"
# make new reminder with properties {name:'gggg', due date: "7/10/2014 3:00 PM"}
# end tell'''
# out = subprocess.run(['osascript', '-e', cmd.encode()], capture_output=True)
# print(out)


# res = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=2021851&appid=b1f0392026be880ca306b077739ebe75&cnt=21&lang=ru")
# data = res.json()
# for i in range(21):
#     print(data['list'][i]['dt_txt'], 'Те'round((int(data['list'][i]['main']['temp'])-32)*(5/9)))
