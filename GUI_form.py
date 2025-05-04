# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame1
###########################################################################

class MainFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Sync iTunes and Windows Media Player Play Counts"), pos = wx.DefaultPosition, size = wx.Size(678, 414), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u"Usage: WMP → iTunes: Update iTunes if WMP>iTunes"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        # RGB for blue
        self.m_staticText2.SetForegroundColour(wx.Colour(0, 0, 255))  
        self.m_staticText2.Wrap( -1 )

        self.m_staticText2.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

        bSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

        RadioBoxOptionsChoices = [ _(u"WMP → iTunes"), _(u"iTunes → WMP"), _(u"Max of iTunes/WMP") ]
        self.RadioBoxOptions = wx.RadioBox( self, wx.ID_ANY, _(u"Target"), wx.DefaultPosition, wx.DefaultSize, RadioBoxOptionsChoices, 1, wx.RA_SPECIFY_COLS )
        self.RadioBoxOptions.SetSelection( 0 )
        bSizer1.Add( self.RadioBoxOptions, 0, wx.ALL, 5 )
         

        self.btn_Sync = wx.Button( self, wx.ID_ANY, _(u"Sync Plays"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_Sync.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )

        bSizer1.Add( self.btn_Sync, 0, wx.ALL, 5 )

        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Results") ), wx.VERTICAL )

        self.OutputWindowCtrl = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_BESTWRAP|wx.TE_MULTILINE|wx.TE_READONLY, wx.DefaultValidator, u"OutputWindow" )
        # sbSizer1.Add( self.OutputWindowCtrl, 0, wx.ALL, 5 )
        sbSizer1.Add(self.OutputWindowCtrl, 1, wx.EXPAND | wx.ALL, 5) 


        bSizer1.Add( sbSizer1, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.btn_Sync.Bind( wx.EVT_BUTTON, self.ChamaSyncFc )

        # PROGRESS BAR
        # Add this right after the Sync button
        # self.progress_bar = wx.Gauge(self, range=100, size=(300, 25))
        # bSizer1.Add(self.progress_bar, 0, wx.EXPAND | wx.ALL, 5)


    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def ChamaSyncFc( self, event ):
        event.Skip()


