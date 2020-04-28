#!/bin/bash
#输入密码不回显
function enterPass()
{
    local PASSWORD=""
    stty -echo #设置输入不回显
    read -p "Please input PASSWORD: " PASSWORD
    echo -e "\r" #换行
    stty echo #取消不回显
    echo "Entered password is $PASSWORD"
}

#输入密码用*代替回显
function EnterPassword()
{
	STTY_RESTORE=$(stty -g)
	echo -n "Password: "
	stty -echo cbreak
	while true
	do
		character=$(dd if=/dev/tty bs=1 count=1 2> /dev/null)
		case $character in
		$(echo -e "\n"))
			break
			;;
		$(echo -e "\b"))
			if [ -n "$password" ]; then
				echo -n -e "\b \b"
				password=$(echo "$password" | sed 's/.$//g')
			fi
			;;
		*)
			password=$password$character
			echo -n '*'
			;;
		esac
	done

	stty $STTY_RESTORE			#stty -cbreak echo
	echo -e "\r"
	echo "inputed password is $password"
}

#enterPass
EnterPassword
