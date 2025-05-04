# THIS IS THE MAIN CODE THAT CALLS THE FORM CODE
# WHICH WAS DESIGNED SEPARATELY IN WxFormBuilder
# IT WILL ALSO CALL THE OTHER CODES

import wx
from GUI_form import MainFrame1  # Import the generated GUI

# from threading import Thread

import sys
sys.path.insert(0, "D:\\Python\\iTunes")
sys.path.insert(0, "D:\\Python\\WMP")

from Read_PL import Init_iTunes, Read_xml, order_list
from WMP_Read_PL import Init_wmp, order_list_wmp, WMP_sel_tags_dict, WMP_all_tags_dict

from os.path import exists

import pandas as pd

# global col_names 
# COLS THAT MATTER FOR THIS PGM 
col_names =  ["Arq", "Plays", "ID"]

# RESIZES THE FORM: bSizer1.Add(self.OutputWindowCtrl, 1, wx.EXPAND | wx.ALL, 5)  (In case form code is overwritten)

# THIS MODULE SETS ARQ TO LOWER CASE FOR THE MERGER
# IT ALSO DEDUPES THE DUPLICATE RECORDS
def df_dedupe(source,df):
    # LOWERCASE THE FILE NAME
    df.loc[:, "Arq"] = df["Arq"].str.lower()

    # ADDS KEY COL. TO DF
    df.loc[:, "max_Plays_" + source] = df.groupby("Arq")["Plays"].transform("max")

    start_rows = df.shape[0]
    # Eliminate duplicate records based on "Arq" (subset=df["Arq"].str.lower() also works)
    df_dedupe = df.drop_duplicates(subset="Arq", keep="first")
    end_rows = df_dedupe.shape[0]
    print("\nThe",source,"df has",start_rows,"tracks before deduping (",end_rows,"after)\n")

    dict = {}
    dict["start_rows"] = start_rows
    dict["end_rows"] = end_rows
    dict["DF"] = df_dedupe
    return dict


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame1(None)
        self.frame.Show()
        # Add this flag
        self.iTunes_launched = False  
        # ADDS A DICTIONARY TO THE CLASS THAT WILL BE USED TO RETURN VALUES (IN ONE OF THE FUNCTIONS)
        # self.result = {}
        
        # Bind button click
        self.frame.btn_Sync.Bind(wx.EVT_BUTTON, self.on_button_click)
        return True

    def on_button_click(self, event):
        # SET TO NONE LATER
        rows = 10000
        
        # Assuming OutputWindowCtrl is a wx.TextCtrl, access it and set the message
        output_text_ctrl = self.frame.OutputWindowCtrl  # Replace with the correct reference to your TextCtrl

        # RADIO BOX: Get the selected radio box index and value (string)
        sel_index = self.frame.RadioBoxOptions.GetSelection()
        selected_radio = self.frame.RadioBoxOptions.GetStringSelection()

        # Display the message
        message = f"\nRadio Box Selected: {selected_radio} (Index: {sel_index})"
        print(message)

        # Now write to the output_text_ctrl
        # output_text_ctrl = self.frame.OutputWindowCtrl  # Reference to the TextCtrl
        # output_text_ctrl.AppendText(message)  # Display the message

        # DON'T DO ANYTHING IF iTunes ALREADY LAUNCHED
        if self.iTunes_launched:
           output_text_ctrl.SetValue("iTunes already launched.")
        
        # Only launch try iTunes once
        if not self.iTunes_launched:        
           output_text_ctrl.SetValue("Launching iTunes...")  # This writes the message into the TextCtrl

           # LAUCH ITUNES (THIS IS JUST TO TEST IF iTunes CAN BE LAUNCHED
           dict = Init_iTunes() 
           success = dict["Success"]

           # THE WHOLE iTunes PROCESS HAS TO HAPPEN HERE 
           if success:
              self.iTunes_launched = True
              iTu_col_names = col_names[:]
              iTu_col_names.append("PID")

              output_text_ctrl.SetValue("Parsing the iTunes XML...")
              iTu_dict = Read_xml(iTu_col_names,rows=rows)

              # ASSIGNS VARS
              iTu_App = iTu_dict["App"]
              iTu_df = iTu_dict["DF"]
              # MAKES A COPY OF THE ORIGINAL PATH LIST ("ARQ")
              iTu_df["Location"] = iTu_df["Arq"].copy()
              # LOWERCASE THE FILE NAME
              iTu_df["Arq"] = iTu_df["Arq"].str.lower()

              # FILES COUNT  
              iTunes_tracks = iTu_df.shape[0]
              output_text_ctrl.SetValue(f"iTunes has {iTunes_tracks} tracks")

              # CHECKING DEAD TRACKS
              output_text_ctrl.SetValue("Checking for missing iTunes tracks")               
              Found = [exists(x) for x in iTu_df["Location"]]
              iTu_df["Found"] = Found

              miss_tracks = Found.count(False)
              output_text_ctrl.SetValue(f"iTunes has {miss_tracks} missing tracks")

              # SELECTS ONLY FOUND FILES
              iTu_df = iTu_df[iTu_df["Found"] == True]
                
              # DROPS DUPES
              output_text_ctrl.SetValue("Deduping iTunes tracks (this may take a while)")
              dict = df_dedupe("iTunes", iTu_df)
              iTu_df = dict["DF"]
              iTu_start_rows = dict["start_rows"]
              iTu_end_rows = dict["end_rows"]
              # output_text_ctrl.SetValue("Deduping iTunes finished...")
              output_text_ctrl.SetValue(f"Finished! From {iTu_start_rows} to {iTu_end_rows} tracks")

              # INIT WMP
              dict = Init_wmp()
              WMP_App = dict['WMP']
              WMP_lib = dict['Library']

              # THIS IS THE LIBRARY
              numtracks = len(WMP_lib) 
              PL_name = "library"
              PL_nbr = 0

              # PROCESS SPECIFIED NUMBER OF ROWS
              if rows is None:
                 numtracks = len(WMP_lib)   
              else:
                  numtracks = min(rows, len(WMP_lib))
                
              # data IS A LIST OF LISTS
              data = []
              output_text_ctrl.SetValue(f"Reading the WMP music library")
              output_text_ctrl.SetValue(f"tracks: {WMP_lib.Count} (processing {numtracks})")
              
              # LOGIC TO DISPLAY IN THE LOG
              tam = max(numtracks // 20, 1)
                
              # ORDER LIST SO COLUMN HEADERS ALIGNS WITH THE VALUES AS THEY WERE APPENDED
              order_col_names = order_list(col_names,order_list=order_list_wmp,Add_cols=True)

              # THE RANGE FOR ITEMS IN A WMP PL IS 0 TO (N-1)
              for m in range(numtracks):
                  track = WMP_lib[m]    

                  # ONLY DOES AUDIO
                  if track.getiteminfo("MediaType")=="audio":
                      # THE SOURCE (PLAYLIST/LIBRARY)
                      tag_list = [PL_nbr,PL_name]
                      # THE TRACK POSITION
                      tag_list.append(m)
                      dict = WMP_sel_tags_dict(track,col_names)
                      for key in order_list(col_names,order_list=order_list_wmp):
                          value = dict[key]
                          tag_list.append(value)
                      #ADD ROW TO LIST, BEFORE CREATING DF
                      data.append(tag_list)
                      if (m+1) % tam==0:
                          print("Row. no: ",m+1,"of",numtracks,"(WMP)")
                          # Yield control to the GUI thread to allow UI updates
                          wx.Yield()
                          perc = (m + 1) / numtracks * 100
                          wx.CallAfter(self.frame.OutputWindowCtrl.SetValue, f"Reading WMP library (completed: {perc:.1f}%)")

              # DATAFRAME
              wx.CallAfter(self.frame.OutputWindowCtrl.SetValue, f"Finished...")
              WMP_df = pd.DataFrame(data, columns=order_col_names)

              # CHANGE DF-ELIMINATE DUPES
              WMP_df = WMP_df.rename(columns={"Pos": "WMP_Pos", "Plays": "max_Plays_WMP"})
              # MAKES THE ARQ COL LOWER CASE TO MATCH THE iTunes DF
              WMP_df.loc[:, "Arq"] = WMP_df["Arq"].str.lower()

              # JOIN THE DATAFRAMES [["Arq", "max_Plays_iTunes", "ID", "Location"]]
              wx.CallAfter(self.frame.OutputWindowCtrl.SetValue, f"Merging iTunes and WMP tracks (may take a while)")
              df = iTu_df.merge(WMP_df[["Arq", "max_Plays_WMP", "WMP_Pos"]], on="Arq", how="inner")

              # XLSX REPORT
              #Save(df,output="Miss_files_merged.xlsx")

              merged_rows = df.shape[0]
              # print("\nThe merged df has",df.shape[0],"tracks")

              # SELECT ONLY RELEVANT ROWS (IN CASE IT"S NOT THE DEAD TRACKS PL)
              if sel_index==0:
                 df = df[df["max_Plays_iTunes"] < df["max_Plays_WMP"]]
              elif sel_index==1:
                 df = df[df["max_Plays_iTunes"] > df["max_Plays_WMP"]]   
              elif sel_index==2:
                 df = df[df["max_Plays_iTunes"] != df["max_Plays_WMP"]]    

              diff_plays = df.shape[0]
              wx.CallAfter(self.frame.OutputWindowCtrl.SetValue, f"There are {diff_plays} tracks where the WMP and iTunes play counts differ!\n")

              # Pop-up a message dialog (wait for user to hit Enter!)
              dlg = wx.MessageDialog(self.frame, "Press Enter to continue...", "Update confirmation", wx.OK | wx.ICON_INFORMATION)
              dlg.ShowModal()
              dlg.Destroy()

              # POPULATES LISTS
              Arq = [x for x in df["Location"]]
              ID = [x for x in df["PID2"]]
              WMP_Pos = [x for x in df["WMP_Pos"]]
              iTunes_plays = [int(x) for x in df["max_Plays_iTunes"]]
              WMP_plays = [x for x in df["max_Plays_WMP"]]
              nbr_files = len(Arq)

              # Get the attribute name from the dictionary
              Plays_attr_name = WMP_all_tags_dict["Plays"]

              print()
              WMP_cnt = 0
              iTu_cnt = 0
              # TRACK METADATA
              cols = ["Art","Title","Genre"]
              # COMPARE AND CHANGE THE FILES
              for i in range(min(1,nbr_files)):
                  iTu_track = iTu_App.LibraryPlaylist.Tracks.ItemByPersistentID(*ID[i])
                  # track_dict = iTunes_sel_tags_dict(iTu_track, cols)
                  # track_meta = track_dict["Art"] +" - "+ track_dict["Title"]
                  
                  # CHANGE TAGS, BOTH ITUNES AND WMP CAN BE UPDATED AT THE SAME TIME NOW (NO LONGER XOR)
                  # MAXIMUM OF THE 3 POSSIBLE SOURCES
                  max_plays = max(iTunes_plays[i], WMP_plays[i])

                  # MESSAGES
                  print()
                  msg = f"\nFile {i+1} of {nbr_files} - track: {Arq[i]} → WMP={WMP_plays[i]} iTunes={iTunes_plays[i]}"
                  print(msg)
                  output_text_ctrl.AppendText(msg)

                  # UPDATE OR NOT?
                  iTu_updt_cnt = iTunes_plays[i]<max_plays
                  WMP_updt_cnt = WMP_plays[i]<max_plays
                  if iTu_updt_cnt or WMP_updt_cnt:
                     print("Updating counts:","iTunes" if iTu_updt_cnt else "","WMP" if WMP_updt_cnt else "")
                  else:
                      print("Not updating counts")   

                  # SETS COUNTS
                  # ITUNES COUNTS
                  if 0 <= iTunes_plays[i] < max_plays:
                       # CHANGE ITUNES TRACK PLAY COUNT
                       print("Doublechecking iTunes plays:",iTu_track.PlayedCount,"// Changing...")
                       iTu_track.PlayedCount = max_plays
                       iTu_cnt = iTu_cnt+1
                    
                  # WMP COUNTS
                  if 0 <= WMP_plays[i] < max_plays:
                     # CHANGE WMP TRACK PLAY COUNT INSTEAD
                     WMP_cnt = WMP_cnt+1
                     WMP_track = WMP_lib.Item(WMP_Pos[i])
                  
                  # TRIES TO RETRIEVE PLAYS
                  plays = WMP_track.getiteminfo("UserPlayCount")
                  # ENSURES THAT THE FILE IS THE SAME
                  if WMP_track.getiteminfo("SourceURL").lower() == Arq[i].lower():
                     print("Doublechecking WMP plays:",plays,"// Changing...", end=" ")
                     WMP_track.setItemInfo("UserPlayCount", max_plays)
                     #WMP_track.setItemInfo("UserPlayCount", str(max_plays))
                     print("(doublecheck WMP count:",WMP_track.getiteminfo("UserPlayCount"),")")
           
           # GIVE UPDATE REFRESHED TAGS 
           print("\nUpdated",WMP_cnt,"Windows Media Player plays")
           print("Updated",iTu_cnt,"iTunes plays")
           output_text_ctrl.AppendText(f"\n\nUpdated {WMP_cnt} WMP plays")
           output_text_ctrl.AppendText(f"\nUpdated {iTu_cnt} iTunes plays\n")

           # QUIT ITUNES TO REFRESH THE XML IF ANY UPDATES TO iTunes were made
           if iTu_cnt>0:
              output_text_ctrl.AppendText(f"\nClosing iTunes to refresh the XML file...")
              iTu_App.Quit()
              self.iTunes_launched = False
           
           if WMP_cnt>0:
              output_text_ctrl.AppendText(f"\nClosing WMP to commit updates...")
              WMP_App.Quit()
              self.iTunes_launched = False

           if not success:
              output_text_ctrl.SetValue("Can't launch iTunes...(close it and retry)")
               
        
# START OF THE CODE
# app = MyApp()
# app.MainLoop()

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
