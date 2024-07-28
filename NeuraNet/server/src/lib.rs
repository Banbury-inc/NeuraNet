mod handlers;
use handlers::database_handler;

pub fn add(left: usize, right: usize) -> usize {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
    #[test]
    fn test_get_total_data_processed() {
        let result = add(2, 2);

        let result2 = database_handler::get_total_data_processed();
        assert_eq!(result, 4);
    }


}


