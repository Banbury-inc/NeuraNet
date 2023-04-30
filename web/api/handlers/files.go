package handlers

import (
	"encoding/json"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"time"

	"github.com/gorilla/mux"
)

// HandleFileUpload handles POST requests to /api/files, which uploads a file.
func HandleFileUpload(w http.ResponseWriter, r *http.Request) {
	// Parse the multipart form data
	err := r.ParseMultipartForm(10 * 1024 * 1024) // 10 MB max file size
	if err != nil {
		http.Error(w, "Error parsing form data", http.StatusBadRequest)
		return
	}

	// Get the uploaded file from the form data
	file, handler, err := r.FormFile("file")
	if err != nil {
		http.Error(w, "Error retrieving file from form data", http.StatusBadRequest)
		return
	}
	defer file.Close()

	// Save the file to disk with a unique filename
	ext := filepath.Ext(handler.Filename)
	filename := strconv.FormatInt(time.Now().Unix(), 10) + ext
	f, err := os.OpenFile("./uploads/"+filename, os.O_WRONLY|os.O_CREATE, 0666)
	if err != nil {
		http.Error(w, "Error saving file to disk", http.StatusInternalServerError)
		return
	}
	defer f.Close()
	_, err = io.Copy(f, file)
	if err != nil {
		http.Error(w, "Error saving file to disk", http.StatusInternalServerError)
		return
	}

	// Respond with the filename
	response := map[string]string{
		"filename": filename,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// HandleFileDownload handles GET requests to /api/files/{filename}, which downloads a file.
func HandleFileDownload(w http.ResponseWriter, r *http.Request) {
	// Get the filename from the URL path
	vars := mux.Vars(r)
	filename := vars["filename"]

	// Open the file on disk
	f, err := os.Open("./uploads/" + filename)
	if err != nil {
		http.Error(w, "Error opening file", http.StatusInternalServerError)
		return
	}
	defer f.Close()

	// Get the file information
	info, err := f.Stat()
	if err != nil {
		http.Error(w, "Error getting file information", http.StatusInternalServerError)
		return
	}
	// Set the response headers
	w.Header().Set("Content-Disposition", "attachment; filename="+filename)
	w.Header().Set("Content-Type", "application/octet-stream")
	w.Header().Set("Content-Length", strconv.FormatInt(info.Size(), 10))

	// Send the file contents to the response writer
	io.Copy(w, f)
}

// handleGetFiles handles GET requests to /api/files, which returns a list of all files.
func handleGetFiles(w http.ResponseWriter, r *http.Request) {
	// TODO: Implement logic to fetch the list of files from storage.
	files := []File{
		{ID: "1", Name: "file1.txt", Size: 1024},
		{ID: "2", Name: "file2.jpg", Size: 2048},
		{ID: "3", Name: "file3.png", Size: 4096},
	}

	// Encode the list of files as JSON and write it to the response.
	w.Header().Set("Content-Type", "application/json")
	err := json.NewEncoder(w).Encode(files)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

// File represents a file in storage.
type File struct {
	ID   string `json:"id"`
	Name string `json:"name"`
	Size int64  `json:"size"`
}

// handleGetFile handles GET requests to /api/file/{id}, which returns the file with the specified ID.
func handleGetFile(w http.ResponseWriter, r *http.Request) {
	// Extract the file ID from the URL parameters.
	vars := mux.Vars(r)
	id := vars["id"]

	// TODO: Implement logic to fetch the file with the specified ID from storage.
	file := File{ID: id, Name: "file.txt", Size: 1024}

	// Encode the file as JSON and write it to the response.
	w.Header().Set("Content-Type", "application/json")
	err := json.NewEncoder(w).Encode(file)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}
