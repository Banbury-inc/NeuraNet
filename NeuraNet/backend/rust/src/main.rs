
mod another_module;

fn second() {
  println!("Second function");
}

fn main() {
  println!("Hello World!");
    second();
    another_module::third();
}


