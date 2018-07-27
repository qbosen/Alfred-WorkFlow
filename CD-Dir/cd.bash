#!/bin/bash


FILE={query}

if [ -d "${FILE}" ]; then     # 目录直接保存
  DIR=${FILE}
else
  if [ -f "${FILE}" ]; then   # 文件获取文件所在目录
    DIR=$(dirname "${FILE}")
  else                        # 其他情况直接退出
    exit 1
  fi
fi


osascript  << END
CommandRun("cd \"${DIR}\"", "Default", "")

on CommandRun(withCmd, withTheme, theTitle)
	tell application "iTerm"
		if it is not running then
			activate
			if (count windows) is 0 then
				NewWin(withTheme) of me
			end if
			SetWinParam(theTitle, withCmd) of me
		else if (count windows) is 0 then
			NewWin(withTheme) of me
			SetWinParam(theTitle, withCmd) of me
		else
			NewTab(withTheme) of me
			SetTabParam(theTitle, withCmd) of me
		end if
		activate
	end tell
end CommandRun

on NewWin(argsTheme)
	tell application "iTerm"
		try
			create window with profile argsTheme
		on error msg
			create window with profile "Default"
		end try
	end tell
end NewWin

on SetWinParam(argsTitle, argsCmd)
	tell application "iTerm"
		tell the current window
			tell the current session
				set name to argsTitle
				write text argsCmd
			end tell
		end tell
	end tell
end SetWinParam

on NewTab(argsTheme)
	tell application "iTerm"
		tell the current window
			try
				create tab with profile withTheme
			on error msg
				create tab with profile "Default"
			end try
		end tell
	end tell
end NewTab

on SetTabParam(argsTitle, argsCmd)
	tell application "iTerm"
		tell the current window
			tell the current tab
				tell the current session
					set name to argsTitle
					write text argsCmd
				end tell
			end tell
		end tell
	end tell
end SetTabParam
END