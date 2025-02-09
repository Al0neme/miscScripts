#!/bin/bash

# file中的内容如果不是git链接，需要指定一个名字作为目录，例如"http://xx.com/dd aa",dd就会保存到aa目录下
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

mapfile -t lines < "$1"

for line in "${lines[@]}"; do
    if [[ "$line" =~ ^http?.*\.git$ ]]; then
        repo_name=$(basename "$line" .git)

        if [ -d "$repo_name" ]; then
            echo "Directory $repo_name already exists, skipping clone."
        else
            echo "Cloning Git repository: $line"
            git clone "$line" > /dev/null 2>&1
            echo "[+] ok"
        fi

    elif [[ "$line" =~ ^http ]]; then

        url=$(echo "$line" | awk '{print $1}')
        dir=$(echo "$line" | awk '{print $2}')
        
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo "Created directory: $dir"
        fi
        
        file_name=$(basename "$url")
        if [ -e "$dir/$file_name" ]; then
            echo "File $file_name already exists in $dir, skipping download."
        else
            echo "Downloading $url to $dir"
            wget -P "$dir" "$url" > /dev/null 2>&1
            echo "[+] ok"
        fi
    else
        echo "Skipping: $line (not a valid Git repo or URL)"
    fi
done
