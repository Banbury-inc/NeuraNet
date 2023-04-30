package handlers

import (
	"io"
	"net/http"

	"github.com/ipfs/go-cid"
	shell "github.com/ipfs/go-ipfs-api"
)

func DownloadHandler(w http.ResponseWriter, r *http.Request) {
	// Connect to local IPFS node
	sh := shell.NewShell("localhost:5001")

	// Get the CID from the query parameters
	query := r.URL.Query()
	cidStr := query.Get("cid")

	// Decode the CID string
	cidObj, err := cid.Decode(cidStr)
	if err != nil {
		http.Error(w, "Invalid CID", http.StatusBadRequest)
		return
	}

	// Download the file from IPFS
	reader, err := sh.Cat(cidObj.String())
	if err != nil {
		http.Error(w, "Error downloading file", http.StatusInternalServerError)
		return
	}

	// Set the Content-Type header based on the file type
	contentType := http.DetectContentType([]byte(cidObj.String()))
	w.Header().Set("Content-Type", contentType)

	// Write the file contents to the response writer
	_, err = io.Copy(w, reader)
	if err != nil {
		http.Error(w, "Error writing file to response", http.StatusInternalServerError)
		return
	}
}
