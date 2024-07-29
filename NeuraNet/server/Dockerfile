# Use the official Rust image as a build stage
FROM rust:latest AS builder

# Set the working directory inside the container
WORKDIR /

# Copy the Cargo.toml and Cargo.lock files
COPY Cargo.toml Cargo.lock ./

# Copy the source code
COPY . .

# Build the application in release mode
RUN cargo build --release

# Use a smaller base image for the final stage
FROM ubuntu:22.04

# Copy the built binary from the builder stage
COPY --from=builder /target/release/server /usr/local/bin/server

# Set the entrypoint
ENTRYPOINT ["server"]

# Expose the port your application runs on
EXPOSE 8080

