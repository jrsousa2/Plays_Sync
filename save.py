# THE PURPOSE OF HAVING THE FUNCTION HERE IS SO THE GUI DOESN'T FREEZE
    # WHEN IT'S RUNNING AND MESSAGES ARE DISPLAYED IN THE GUI AS IT RUNS
    # SINCE THIS FUNCTION WILL EXECUTE FROM A THREAD, IT CAN'T RETURN VALUES
    # RETURNED VALUES WILL BE IN THE CLASS
    def Read_WMP_library(self, rows):
        # INIT WMP
        dict = Init_wmp()
        wmp = dict['WMP']
        library = dict['Library']

        # THIS IS THE LIBRARY
        numtracks = len(library) 
        PL_name = "library"
        PL_nbr = 0

        # PROCESS SPECIFIED NUMBER OF ROWS
        if rows is None:
           numtracks = len(library)   
        else:
            numtracks = min(rows, len(library))
        
        # data IS A LIST OF LISTS
        data = []
        wx.CallAfter(self.frame.OutputWindowCtrl.SetValue, f"Reading the WMP music library")
        wx.CallAfter(self.frame.OutputWindowCtrl.SetValue, f"\ntracks: ",library.Count,"(processing",numtracks,")")

        # LOGIC TO DISPLAY IN THE LOG
        tam = max(numtracks // 20, 1)
        
        # ORDER LIST SO COLUMN HEADERS ALWAYS MATCH THEIR VALUES
        col_names = order_list(col_names,order_list=order_list_wmp)
        # THE RANGE FOR ITEMS IN A WMP PL IS 0 TO (N-1)
        for m in range(numtracks):
            track = library[m]    
            
            # ONLY DOES AUDIO
            if track.getiteminfo("MediaType")=="audio":
                # THE SOURCE (PLAYLIST/LIBRARY)
                tag_list = [PL_nbr,PL_name]
                # THE TRACK POSITION
                tag_list.append(m)
                dict = WMP_tag_dict(track,col_names)
                for key in col_names:
                    value = dict[key]
                    tag_list.append(value)
                #ADD ROW TO LIST, BEFORE CREATING DF
                data.append(tag_list)
                if (m+1) % tam==0:
                    # print("Row no: ",m+1)
                    wx.CallAfter(self.frame.OutputWindowCtrl.SetValue, f"Processed {m} of {numtracks} files...")

        # DATAFRAME
        # ORDER THE LIST SO COLUMN HEADERS MATCH THEIR VALUES
        order_col_names = order_list(col_names,order_list=order_list_wmp)
        df = pd.DataFrame(data, columns=order_col_names)

        # RETURN ALL RELEVANT OBJS
        self.result['WMP'] = wmp
        self.result['Lib'] = library
        self.result['DF'] = df
        # dict = {"WMP": wmp, "Lib": library, "DF": df}
        # return dict

        # ONLY USED TO DEBUG, NOT BEING USED ANYMORE
def Save(df,output="iTunes_vs_WMP.xlsx"):
    # SAVE TO EXCEL FILE:
    file_nm = "D:\\Python\\Excel\\" + output
    # save the dataframe to an Excel file
    df.to_excel(file_nm, index=False)

            #   Save(WMP_df,output="WMP.xlsx")
            #   Save(iTu_df,output="iTunes.xlsx")

              # XLSX REPORT
              # Save(df,output="Miss_files_merged.xlsx")