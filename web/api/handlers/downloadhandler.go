package handlers

import (
	"fmt"
	"io"
	"mime"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

func DownloadHandler(w http.ResponseWriter, r *http.Request) {
	// Get the CID of the file to download
	var cid string
	fmt.Print("Enter the CID of the file to download: ")
	fmt.Scanln(&cid)

	// Download the file from IPFS
	res, err := http.Get(fmt.Sprintf("https://ipfs.io/ipfs/%s", cid))
	if err != nil {
		fmt.Printf("Error downloading file: %v\n", err)
		return
	}
	defer res.Body.Close()
	if res.StatusCode != http.StatusOK {
		fmt.Printf("Unexpected status code: %d\n", res.StatusCode)
		return
	}

	// Get the filename and file type from the Content-Disposition header
	filename := ""
	contentType := ""
	contentDisposition := res.Header.Get("Content-Disposition")
	if contentDisposition != "" {
		_, params, err := mime.ParseMediaType(contentDisposition)
		if err == nil {
			filename = params["filename"]
			contentType = params["type"]
		}
	}

	// Prompt the user to save the file to their computer
	if filename == "" {
		fmt.Print("Enter a filename for the downloaded file: ")
		fmt.Scanln(&filename)
		contentType = mime.TypeByExtension(filepath.Ext(filename))
	}
	filePath := filepath.Join(os.Getenv("HOME"), "Downloads", filename)
	file, err := os.Create(filePath)
	if err != nil {
		fmt.Printf("Error creating file: %v\n", err)
		return
	}
	defer file.Close()
	if _, err := io.Copy(file, res.Body); err != nil {
		fmt.Printf("Error writing file to disk: %v\n", err)
		return
	}

	if contentType != "" {
		if err := os.Rename(filePath, filePath+"."+strings.Split(contentType, "/")[1]); err != nil {
			fmt.Printf("Error renaming file: %v\n", err)
			return
		}
		filePath += "." + strings.Split(contentType, "/")[1]
	}

	fmt.Printf("File downloaded and saved to %s\n", filePath)
}
