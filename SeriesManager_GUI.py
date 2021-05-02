#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.6 on Tue Dec 29 14:59:27 2020
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class SeriesManager(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: SeriesManager.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((744, 622))
        self.btnSetRegistry = wx.Button(self, wx.ID_ANY, u"레지스트리 등록")
        self.btnRemoveRegistry = wx.Button(self, wx.ID_ANY, u"레지스트리 제거")
        self.btnYoutube = wx.Button(self, wx.ID_ANY, u"유튜브 채널")
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.lbCurrentLocation = wx.StaticText(self.panel_1, wx.ID_ANY, "C:\\")
        self.panel_2 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.listVideoFiles = wx.ListBox(self.panel_2, wx.ID_ANY, choices=[], style=wx.LB_HSCROLL | wx.LB_SINGLE)
        self.btnVideoUp = wx.Button(self.panel_2, wx.ID_ANY, "Up")
        self.btnVideoDown = wx.Button(self.panel_2, wx.ID_ANY, "Down")
        self.btnVideoDelete = wx.Button(self.panel_2, wx.ID_ANY, "Delete")
        self.listSubtitleFiles = wx.ListBox(self.panel_2, wx.ID_ANY, choices=[], style=wx.LB_HSCROLL | wx.LB_SINGLE)
        self.btnSubtitleUp = wx.Button(self.panel_2, wx.ID_ANY, "Up")
        self.btnSubtitleDown = wx.Button(self.panel_2, wx.ID_ANY, "Down")
        self.btnSubtitleDelete = wx.Button(self.panel_2, wx.ID_ANY, "Delete")
        self.rbVideo = wx.RadioButton(self.panel_1, wx.ID_ANY, "")
        self.lbRadioVideo = wx.StaticText(self.panel_1, wx.ID_ANY, u"비디오 파일명에 맞추기")
        self.rbSubtitle = wx.RadioButton(self.panel_1, wx.ID_ANY, "")
        self.lbRadioSubtitle = wx.StaticText(self.panel_1, wx.ID_ANY, u"자막 파일명에 맞추기")
        self.rbNew = wx.RadioButton(self.panel_1, wx.ID_ANY, "")
        self.lbRadioNew = wx.StaticText(self.panel_1, wx.ID_ANY, u"새로운 이름규칙으로 맞추기")
        self.tbRule = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.btnProceed = wx.Button(self.panel_1, wx.ID_ANY, u"일괄수정")
        self.btnRestore = wx.Button(self.panel_1, wx.ID_ANY, u"복원")
        self.tbSync = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.btnSync = wx.Button(self.panel_1, wx.ID_ANY, u"자막싱크 일괄수정")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: SeriesManager.__set_properties
        self.SetTitle(u"시리즈 매니저 (by 개발자 라라)")
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.rbVideo.SetValue(1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: SeriesManager.__do_layout
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.btnSetRegistry, 1, 0, 0)
        sizer_4.Add(self.btnRemoveRegistry, 1, 0, 0)
        sizer_4.Add(self.btnYoutube, 1, 0, 0)
        sizer_2.Add(sizer_4, 0, wx.EXPAND, 0)
        label_4 = wx.StaticText(self.panel_1, wx.ID_ANY, u"현재 위치: ")
        sizer_8.Add(label_4, 0, 0, 0)
        sizer_8.Add(self.lbCurrentLocation, 1, 0, 0)
        sizer_3.Add(sizer_8, 0, wx.EXPAND, 0)
        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, "Video Files")
        sizer_7.Add(label_1, 1, wx.RIGHT, 5)
        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, "Subtitle Files")
        sizer_7.Add(label_2, 1, wx.LEFT, 5)
        sizer_3.Add(sizer_7, 0, wx.EXPAND | wx.TOP, 5)
        sizer_5.Add(self.listVideoFiles, 1, wx.EXPAND | wx.FIXED_MINSIZE, 0)
        sizer_9.Add(self.btnVideoUp, 0, 0, 0)
        sizer_9.Add(self.btnVideoDown, 0, 0, 0)
        sizer_9.Add(self.btnVideoDelete, 0, 0, 0)
        sizer_5.Add(sizer_9, 0, wx.EXPAND | wx.RIGHT, 5)
        sizer_5.Add(self.listSubtitleFiles, 1, wx.EXPAND | wx.FIXED_MINSIZE | wx.LEFT, 5)
        sizer_10.Add(self.btnSubtitleUp, 0, 0, 0)
        sizer_10.Add(self.btnSubtitleDown, 0, 0, 0)
        sizer_10.Add(self.btnSubtitleDelete, 0, 0, 0)
        sizer_5.Add(sizer_10, 0, wx.EXPAND, 0)
        self.panel_2.SetSizer(sizer_5)
        sizer_3.Add(self.panel_2, 1, wx.EXPAND, 0)
        sizer_11.Add(self.rbVideo, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_11.Add(self.lbRadioVideo, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_11.Add(self.rbSubtitle, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 20)
        sizer_11.Add(self.lbRadioSubtitle, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_11.Add(self.rbNew, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 20)
        sizer_11.Add(self.lbRadioNew, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_3.Add(sizer_11, 0, wx.EXPAND | wx.TOP, 5)
        label_8 = wx.StaticText(self.panel_1, wx.ID_ANY, u"새로운 이름규칙 (파일명을 입력해주세요 숫자를 넣고 싶은 부분에 %d 를 넣어주세요, 넣지 않으면 자동으로 마지막에 붙습니다")
        sizer_3.Add(label_8, 0, wx.TOP, 10)
        sizer_1.Add(self.tbRule, 1, wx.EXPAND, 0)
        sizer_1.Add(self.btnProceed, 0, 0, 0)
        sizer_1.Add(self.btnRestore, 0, 0, 0)
        sizer_3.Add(sizer_1, 0, wx.EXPAND, 0)
        label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, u"자막 싱크 일괄 조정 (smi 만 가능)")
        sizer_3.Add(label_3, 0, wx.TOP, 10)
        sizer_6.Add(self.tbSync, 1, wx.EXPAND, 0)
        sizer_6.Add(self.btnSync, 0, 0, 0)
        sizer_3.Add(sizer_6, 0, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_3)
        sizer_2.Add(self.panel_1, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer_2)
        self.Layout()
        # end wxGlade

# end of class SeriesManager

class MyApp(wx.App):
    def OnInit(self):
        self.frame = SeriesManager(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
