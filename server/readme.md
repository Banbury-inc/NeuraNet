# to allow unprivileged users to bind to ports below 1024,
# you can set this parameter to a lower value

sudo sysctl -w net.ipv4.ip_unprivileged_port_start=0


# compile as an executable

cargo build --release

# run the executable

./NeuraNet/server/target/release/server




