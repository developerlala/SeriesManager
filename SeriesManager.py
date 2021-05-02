import re
import webbrowser

import wx
import os
import datetime
import json
import magic
import sys
import winreg
import ctypes
import win32api

from inspect import getsourcefile
from os.path import abspath
from os import listdir
from SeriesManager_GUI import SeriesManager
from shutil import copyfile
from datetime import datetime


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def rename(_from, _to):
    os.rename(_from, _to)


def file_put_contents(filename, contents):
    if os.path.isfile(filename):
        os.remove(filename)

    f = open(filename, 'w', encoding='UTF-8')
    f.write(contents)
    f.close()


def file_get_contents(filename):
    blob = open(filename, 'rb').read()
    m = magic.Magic(mime_encoding=True)
    encoding = m.from_buffer(blob)

    s = open(filename, 'rt', encoding=encoding).read(-1)
    str(s.encode())

    return s


def path_join(p1, p2):
    if p1[-1] == '/':
        left = p1[:p1.len - 1]
    else:
        left = p1

    if p2[0] == '/':
        right = p2[1:]
    else:
        right = p2

    return left + '/' + right


def isSubtitle(file):
    exts = ['.smi', '.srt', '.ass']
    for ext in exts:
        if file.endswith(ext): return True
    return False


def isVideo(file):
    exts = ['.mkv', '.mp4', '.avi']
    for ext in exts:
        if file.endswith(ext): return True
    return False


def fileRename(fromNameWithExt, toNameWithoutExt, path):
    name, ext = os.path.splitext(fromNameWithExt)
    _from = name + ext
    _to = toNameWithoutExt + ext
    rename(path_join(path, _from), path_join(path, _to))

    print('from:' + _from + ' to:' + _to)
    return name + ext, _to


def restore(path):
    path_log = path_join(path, 'backup')
    files = listdir(path_log)
    files.sort(reverse=True)

    targetFile = path_join(path_log, files[0])

    with open(targetFile) as json_file:
        json_data = json.load(json_file)
        if json_data['__work__'] == 'rename':
            del json_data['__work__']
            for key in json_data:
                _from = json_data[key]
                _to = key

                rename(path_join(path, _from), path_join(path, _to))

        elif json_data['__work__'] == 'sync':
            del json_data['__work__']
            pass


def changeNames(subtitles, videos, namebase, path, numberStart=0, option=0):
    now = datetime.now()
    logfilename = now.strftime('%Y%m%d-%H%M%S') + '.log'
    logfilepath = path_join(path, 'backup')

    if not os.path.isdir(logfilepath):
        os.makedirs(logfilepath)

    number = numberStart

    log = {}

    if option == 0:  # Video 기준 Subtitle 변경
        for i in range(0, len(videos)):
            _name, _ext = os.path.splitext(videos[i])
            _from, _to = fileRename(subtitles[i], _name, path)
            log[_from] = _to
    elif option == 1:  # Subtitle 기준 Video 변경
        for i in range(0, len(videos)):
            _name, _ext = os.path.splitext(subtitles[i])
            _from, _to = fileRename(videos[i], _name, path)
            log[_from] = _to
    else:  # 새 이름으로 변경
        for subtitle in subtitles:
            _from, _to = fileRename(subtitle, namebase % number, path)
            log[_from] = _to
            number += 1

        number = numberStart
        for video in videos:
            _from, _to = fileRename(video, namebase % number, path)
            log[_from] = _to
            number += 1

    log['__work__'] = 'rename'

    logstring = json.dumps(log, indent=4)
    file_put_contents(path_join(logfilepath, logfilename), logstring)
    print(logstring)


def setSync(currentDirectory, subtitles, syncMillisec):
    list = {}

    for smi in subtitles:
        backupPath = path_join(currentDirectory, 'backup')
        time = datetime.now().strftime("%Y%m%d-%H%M%S")

        if not smi.endswith(".smi"):
            print("subitle file is not smi file")
            continue

        list[smi] = path_join('backup', smi) + "." + time + ".bak"

        if not os.path.isdir(backupPath):
            os.mkdir(backupPath)

        copyfile(path_join(currentDirectory, smi), path_join(backupPath, smi + "." + time + ".bak"))

        s = file_get_contents(path_join(currentDirectory, smi))
        pattern = '<Sync\s+Start\s*=\s*[0-9]+'
        p = re.compile(pattern, re.IGNORECASE)
        ret = p.findall(s)

        for item in ret:
            p = re.compile('[0-9]+').search(item)
            s = s.replace(item, '<Sync Start=%d' % (int(p.group()) + syncMillisec))

        file_put_contents(path_join(currentDirectory, smi), s)

    list["__work__"] = "sync"

    logfilepath = datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"
    logfilepath = path_join(backupPath, logfilepath)
    file_put_contents(logfilepath, json.dumps(list, indent=4))


def setRegistryValueHKCR(path: str, valueName: str, value: str):
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, path)
    winreg.SetValueEx(key, valueName, 0, winreg.REG_SZ, value)


def setRegistry():
    if os.name != 'nt':
        return

    print(abspath(getsourcefile(lambda: 0)))
    print(sys.argv[0])

    filename = sys.argv[0]
    filename = filename.replace('\\', '/')
    cwp = path_join(os.getcwd(), filename[filename.rindex('/'):])
    cwp = cwp.replace('/', '\\')

    menuName = "Series Manager"

    setRegistryValueHKCR(r"Directory\Background\shell\SeriesManager", "", menuName)
    setRegistryValueHKCR(r"Directory\Background\shell\SeriesManager", "Icon", cwp)
    setRegistryValueHKCR(r"Directory\Background\shell\SeriesManager\command", "", cwp + ' "%V')

    setRegistryValueHKCR(r"Directory\shell\SeriesManager", "", menuName)
    setRegistryValueHKCR(r"Directory\shell\SeriesManager", "Icon", cwp)
    setRegistryValueHKCR(r"Directory\shell\SeriesManager\command", "", cwp + ' "%1"')

    setRegistryValueHKCR(r"*\shell\SeriesManager", "", menuName)
    setRegistryValueHKCR(r"*\shell\SeriesManager", "Icon", cwp)
    setRegistryValueHKCR(r"*\shell\SeriesManager\command", "", cwp + ' "%1"')


def removeRegistryIfExists(path: str):
    if os.name != 'nt':
        return
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, path)
    except:
        pass


def removeRegistry():
    removeRegistryIfExists(r"Directory\Background\shell\SeriesManager\command")
    removeRegistryIfExists(r"Directory\Background\shell\SeriesManager")
    removeRegistryIfExists(r"Directory\shell\SeriesManager\command")
    removeRegistryIfExists(r"Directory\shell\SeriesManager")
    removeRegistryIfExists(r"*\shell\SeriesManager\command")
    removeRegistryIfExists(r"*\shell\SeriesManager")


class SeriesManagerBody(SeriesManager):
    def __init__(self, *args, **kw):
        super(SeriesManagerBody, self).__init__(*args, **kw)

        self.SetMinSize((800, 600))
        self.SetMaxSize((1280, 720))

        self.currentDirectory = ""
        self.subtitles = []
        self.videos = []

        self.btnVideoUp.Bind(wx.EVT_BUTTON, self.onClickBtnVideoUp)
        self.btnVideoDown.Bind(wx.EVT_BUTTON, self.onClickBtnVideoDown)
        self.btnSubtitleUp.Bind(wx.EVT_BUTTON, self.onClickBtnSubtitleUp)
        self.btnSubtitleDown.Bind(wx.EVT_BUTTON, self.onClickBtnSubtitleDown)
        self.btnVideoDelete.Bind(wx.EVT_BUTTON, self.onClickBtnVideoDelete)
        self.btnSubtitleDelete.Bind(wx.EVT_BUTTON, self.onClickBtnSubtitleDelete)
        self.btnSync.Bind(wx.EVT_BUTTON, self.onClickBtnSync)
        self.btnProceed.Bind(wx.EVT_BUTTON, self.onClickBtnProceed)
        self.btnRestore.Bind(wx.EVT_BUTTON, self.onClickBtnRestore)
        self.tbRule.Disable()
        self.Bind(wx.EVT_RADIOBUTTON, self.onClickRadioButton)
        self.btnSetRegistry.Bind(wx.EVT_BUTTON, self.onClickBtnSetRegistry)
        self.btnRemoveRegistry.Bind(wx.EVT_BUTTON, self.onClickBtnRemoveRegistry)
        self.btnYoutube.Bind(wx.EVT_BUTTON, self.onClickBtnYoutube)
        # self.SetIcon(wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO))
        exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
        icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.Center()

    def onClickRadioButton(self, e):
        if e.GetEventObject() == self.rbVideo:
            self.tbRule.Disable()
        elif e.GetEventObject() == self.rbSubtitle:
            self.tbRule.Disable()
        else:
            self.tbRule.Enable()

    def setDirectory(self, directory: str):
        if directory == '':
            dlg = wx.DirDialog(None, "Choose input directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
            dlg.ShowModal()
            directory = dlg.GetPath()

        self.currentDirectory = directory
        self.lbCurrentLocation.SetLabelText(directory)
        self.subtitles.clear()
        self.videos.clear()

        if os.path.isdir(directory):
            for file in listdir(directory):
                if isSubtitle(file): self.subtitles.append(file)
                if isVideo(file): self.videos.append(file)
            self.subtitles.sort(key=lambda f: int(re.sub('\D', '', f)))
            self.videos.sort(key=lambda f: int(re.sub('\D', '', f)))
            self.refreshList()

        if directory == '' or len(self.subtitles) == 0 or len(self.videos) == 0:
            self.btnSync.Disable()
            self.btnProceed.Disable()
            self.btnRestore.Disable()
            self.rbNew.Disable()
            self.rbVideo.Disable()
            self.rbSubtitle.Disable()
            return

    def refreshList(self):
        self.listVideoFiles.Clear()
        self.listSubtitleFiles.Clear()

        for item in self.subtitles:
            self.listSubtitleFiles.Append(item)
        for item in self.videos:
            self.listVideoFiles.Append(item)

    def swapItem(self, list, index1, index2):
        list[index1], list[index2] = list[index2], list[index1]

    def onClickBtnVideoUp(self, e: wx.Event):
        selection = self.listVideoFiles.GetSelection()
        if selection == wx.NOT_FOUND or selection == 0:
            return
        self.swapItem(self.videos, selection - 1, selection)
        self.refreshList()
        self.listVideoFiles.SetSelection(selection - 1)

    def onClickBtnVideoDown(self, e: wx.Event):
        selection = self.listVideoFiles.GetSelection()
        if selection == wx.NOT_FOUND or selection == len(self.videos) - 1:
            return
        self.swapItem(self.videos, selection, selection + 1)
        self.refreshList()
        self.listVideoFiles.SetSelection(selection + 1)

    def onClickBtnSubtitleUp(self, e: wx.Event):
        selection = self.listSubtitleFiles.GetSelection()
        if selection == wx.NOT_FOUND or selection == 0:
            return
        self.swapItem(self.subtitles, selection - 1, selection)
        self.refreshList()
        self.listSubtitleFiles.SetSelection(selection - 1)

    def onClickBtnSubtitleDown(self, e: wx.Event):
        selection = self.listSubtitleFiles.GetSelection()
        if selection == wx.NOT_FOUND or selection == len(self.subtitles) - 1:
            return
        self.swapItem(self.subtitles, selection, selection + 1)
        self.refreshList()
        self.listSubtitleFiles.SetSelection(selection + 1)

    def onClickBtnVideoDelete(self, e: wx.Event):
        selection = self.listVideoFiles.GetSelection()
        if selection == wx.NOT_FOUND:
            return
        self.videos.remove(self.videos[selection])
        self.refreshList()

    def onClickBtnSubtitleDelete(self, e: wx.Event):
        selection = self.listSubtitleFiles.GetSelection()
        if selection == wx.NOT_FOUND:
            return
        self.subtitles.remove(self.subtitles[selection])
        self.refreshList()

    def onClickBtnSync(self, e: wx.Event):
        try:
            value = int(self.tbSync.GetLineText(0))
            ++value
            print(value)
        except:
            wx.MessageBox("숫자를 밀리초 단위로 입력해주세요, (1000 = 1초)", "오류")
            return

        setSync(
            currentDirectory=self.currentDirectory,
            subtitles=self.subtitles,
            syncMillisec=value
        )
        self.tbSync.SetLabelText("")
        wx.MessageBox("싱크수정 완료", "알림")

    def onClickBtnProceed(self, e: wx.Event):
        if len(self.videos) != len(self.subtitles):
            wx.MessageBox("비디오의 개수와, 자막의 개수가 일치하지 않습니다", "오류")
            return

        filename = self.tbRule.GetLineText(0)

        if self.rbVideo.GetValue():
            changeNames(
                subtitles=self.subtitles,
                videos=self.videos,
                namebase="",
                path=self.currentDirectory,
                numberStart=1,
                option=0
            )
        elif self.rbSubtitle.GetValue():
            changeNames(
                subtitles=self.subtitles,
                videos=self.videos,
                namebase="",
                path=self.currentDirectory,
                numberStart=1,
                option=1
            )
        else:
            if not isinstance(filename, str) or filename == '':
                wx.MessageBox("파일명을 입력하지 않았습니다", "오류")
                return

            if filename and filename.find("%d") == -1:
                filename = filename + "%d"

            result = wx.MessageBox("다음으로 입력하신 파일명이 맞나요?\n" + filename, "확인", wx.OK | wx.CANCEL)

            if result == wx.CANCEL:
                return

            filename = filename.replace("%d", "%02d")

            changeNames(
                subtitles=self.subtitles,
                videos=self.videos,
                namebase=filename,
                path=self.currentDirectory,
                numberStart=1,
                option=2
            )
        wx.MessageBox("변환 완료", "알림")
        self.tbRule.SetLabelText("")
        self.setDirectory(self.currentDirectory)

    def onClickBtnRestore(self, e: wx.Event):
        backup_path = path_join(self.currentDirectory, 'backup')
        files = os.listdir(backup_path)
        files.sort(reverse=True)
        log_file = ""
        for file in files:
            if file.endswith(".log"):
                log_file = path_join(backup_path, file)
                break
        if log_file == "":
            wx.MessageBox("복원할 파일이 없습니다", "알림")
            return

        json_str = file_get_contents(log_file)

        obj = json.loads(json_str)
        if not ('__work__' in obj):
            return

        work = obj.pop('__work__')
        print(work)

        if work == "sync":
            for key in obj:
                original = key
                backup_file = obj[key]
                os.remove(path_join(self.currentDirectory, original))
                os.rename(path_join(self.currentDirectory, backup_file), path_join(self.currentDirectory, original))

        elif work == "rename":
            for key in obj:
                original = key
                renamed = obj[key]
                os.rename(path_join(self.currentDirectory, renamed), path_join(self.currentDirectory, original))

        os.remove(log_file)
        wx.MessageBox("복원 완료", "알림")
        self.setDirectory(self.currentDirectory)

    def onClickBtnSetRegistry(self, e):
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            self.Close()
            return

        setRegistry()
        wx.MessageBox("레지스트리 등록 성공", "알림")

    def onClickBtnRemoveRegistry(self, e):
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            self.Close()
            return

        removeRegistry()
        wx.MessageBox("레지스트리 삭제 성공", "알림")

    def onClickBtnYoutube(self, e):
        webbrowser.open('https://youtube.com/c/devlala')


def main():
    app = wx.App()
    ex = SeriesManagerBody(None)
    ex.Show()

    directory = sys.argv[1] if len(sys.argv) >= 2 else ""
    directory = directory.replace('\\', '/')

    if os.path.isfile(directory):
        directory = directory[0:directory.rindex('/')]
    ex.setDirectory(directory)


    app.MainLoop()


if __name__ == '__main__':
    main()
