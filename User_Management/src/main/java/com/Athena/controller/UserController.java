@RestController
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<String> registerUser(@RequestBody User user) {
        // Implement user registration logic and save the user to the database
        return ResponseEntity.ok("User registered successfully");
    }

    @PostMapping("/login")
    public ResponseEntity<String> loginUser(@RequestBody User user) {
        // Implement user login logic and return a JWT token upon successful login
        return ResponseEntity.ok("User logged in successfully");
    }

    @GetMapping("/profile/{userId}")
    public ResponseEntity<User> getUserProfile(@PathVariable Long userId) {
        // Fetch user profile data from the database and return it
        User user = userService.getUserById(userId);
        return ResponseEntity.ok(user);
    }
}
