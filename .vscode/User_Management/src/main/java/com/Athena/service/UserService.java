package main.java.com.Athena.service;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public User getUserById(Long userId) {
        // Fetch user from the database using UserRepository
        return userRepository.findById(userId).orElse(null);
    }

    // Other service methods for user registration, login, etc.
}

