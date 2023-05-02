package handlers

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"

	shell "github.com/ipfs/go-ipfs-api"
)

type PageData struct {
	Title   string
	Static  string
	Content template.HTML
	FileCID string
}

func UploadHandler(w http.ResponseWriter, r *http.Request) {
	// Connect to local IPFS node
	sh := shell.NewShell("localhost:5001")

	// Check if the connection was successful
	if _, err := sh.ID(); err != nil {
		fmt.Println("Failed to connect to IPFS node")
	} else {
		fmt.Println("Connection successful!")
	}

	// Get the uploaded file from the request
	file, _, err := r.FormFile("file")
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	defer file.Close()

	// Upload file to IPFS
	cid, err := sh.Add(file)
	if err != nil {
		log.Fatalf("Error uploading file: %v", err)
	}

	// Set the page data
	pageData := PageData{
		Title:   "File Upload",
		Static:  "/static",
		Content: "",
		FileCID: cid,
	}
	// Read the existing HTML page
	existingPage, err := ioutil.ReadFile("web/ui/templates/upload.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Set the response headers
	w.Header().Add("Content-Type", "text/html; charset=utf-8")
	w.WriteHeader(http.StatusOK)

	// Write the existing page to the response writer
	fmt.Fprintf(w, string(existingPage))

	// Write the HTML page to the response writer
	fmt.Fprintf(w, "<!DOCTYPE html>\n")
	fmt.Fprintf(w, "<html>\n")
	fmt.Fprintf(w, "<head>\n")
	fmt.Fprintf(w, "<meta charset=\"utf-8\">\n")

	fmt.Fprintf(w, "</head>\n")
	fmt.Fprintf(w, "<body>\n")

	// Write the file CID as a label
	fmt.Fprintf(w, "<label>File uploaded successfully with CID %s</label>\n", pageData.FileCID)

	fmt.Fprintf(w, "</body>\n")
	fmt.Fprintf(w, "</html>\n")

}
