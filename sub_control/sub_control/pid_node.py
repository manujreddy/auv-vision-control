import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class PIDDepthController(Node):
    def __init__(self):
        super().__init__('pid_node')
        
        # Publishers and Subscribers
        self.cmd_pub = self.create_publisher(Float32, '/motor_cmd', 10)
        self.current_depth_sub = self.create_subscription(Float32, '/current_depth', self.depth_callback, 10)
        self.target_depth_sub = self.create_subscription(Float32, '/target_depth', self.target_callback, 10)
        
        # State variables
        self.current_depth = 0.0
        self.target_depth = 0.0
        
        # PID Constants (These are baseline numbers we can tune later)
        self.kp = 2.0
        self.ki = 0.1
        self.kd = 0.5
        
        self.prev_error = 0.0
        self.integral = 0.0
        
        # Control loop timer (runs 10 times a second)
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info("PID Depth Controller Started!")

    def depth_callback(self, msg):
        self.current_depth = msg.data

    def target_callback(self, msg):
        self.target_depth = msg.data

    def control_loop(self):
        # Calculate error (Distance to target)
        error = self.target_depth - self.current_depth
        
        # Proportional, Integral, and Derivative math
        self.integral += error * 0.1  # 0.1 is the timer period
        derivative = (error - self.prev_error) / 0.1
        
        # Compute final motor output speed
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        # Save current error for the next loop's derivative calculation
        self.prev_error = error
        
        # Publish motor command
        cmd_msg = Float32()
        cmd_msg.data = output
        self.cmd_pub.publish(cmd_msg)
        
        # Print to terminal so we can see what it's doing
        self.get_logger().info(f"Target: {self.target_depth:.2f} | Current: {self.current_depth:.2f} | Motor Cmd: {output:.2f}")

def main(args=None):
    rclpy.init(args=args)
    node = PIDDepthController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()