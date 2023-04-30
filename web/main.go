package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"mymodule/web/api/handlers"
	"net/http"
	"path/filepath"
)

func main() {
	// Serve static files
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	// Set up templates
	templates, err := template.ParseGlob(filepath.Join("web/ui/templates", "*.html"))
	if err != nil {
		log.Fatalf("Error parsing templates: %v", err)
	}

	// Set up routes
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/" || r.URL.Path == "/home.html" {
			data := struct {
				Title string
			}{
				Title: "Home",
			}
			if err := templates.ExecuteTemplate(w, "base.html", data); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
			}
		} else if r.URL.Path == "/signup.html" {
			data := struct {
				Title string
			}{
				Title: "Signup",
			}
			if err := templates.ExecuteTemplate(w, "signup.html", data); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
			}
		} else if r.URL.Path == "/upload.html" {
			data := struct {
				Title string
			}{
				Title: "Upload",
			}
			if err := templates.ExecuteTemplate(w, "upload.html", data); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
			}
		} else {
			// Serve the file content when a link is clicked
			filePath := filepath.Join("static", r.URL.Path)
			fileContent, err := ioutil.ReadFile(filePath)
			if err != nil {
				http.Error(w, fmt.Sprintf("Error reading file: %v", err), http.StatusInternalServerError)
				return
			}
			data := struct {
				Title string
				Body  template.HTML
			}{
				Title: r.URL.Path,
				Body:  template.HTML(fileContent),
			}
			if err := templates.ExecuteTemplate(w, "base.html", data); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
			}
		}
	})

	http.HandleFunc("/upload", handlers.UploadHandler)

	// Start server
	log.Println("Starting server on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("Error starting server: %v", err)
	}
}
