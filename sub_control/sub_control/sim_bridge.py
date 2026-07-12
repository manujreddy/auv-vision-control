import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from visualization_msgs.msg import Marker
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

class SimBridge(Node):
    def __init__(self):
        super().__init__('sim_bridge')
        # Talk to PID node
        self.depth_pub = self.create_publisher(Float32, '/current_depth', 10)
        self.motor_sub = self.create_subscription(Float32, '/motor_cmd', self.motor_callback, 10)
        
        # Talk to RViz2 (Digital Twin)
        self.tf_broadcaster = TransformBroadcaster(self)
        self.marker_pub = self.create_publisher(Marker, '/auv_marker', 10)
        
        self.current_depth = 0.0
        self.motor_cmd = 0.0
        
        self.timer = self.create_timer(0.1, self.physics_loop)
        self.get_logger().info("RViz Digital Twin Bridge Started!")

    def motor_callback(self, msg):
        self.motor_cmd = msg.data

    def physics_loop(self):
        # 1. Physics Math: Motor thrust changes our depth
        self.current_depth += (self.motor_cmd * 0.01)

        # 2. Publish depth back to PID
        depth_msg = Float32()
        depth_msg.data = self.current_depth
        self.depth_pub.publish(depth_msg)

        # 3. Broadcast the coordinate frame to RViz
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'base_link'
        t.transform.translation.z = -self.current_depth
        t.transform.rotation.w = 1.0
        self.tf_broadcaster.sendTransform(t)
        
        # 4. Draw a 3D blue box exactly at those coordinates
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "auv"
        marker.id = 0
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.pose.position.z = 0.0
        marker.pose.orientation.w = 1.0
        marker.scale.x = 0.6  # Length
        marker.scale.y = 0.3  # Width
        marker.scale.z = 0.2  # Height
        marker.color.r = 0.0
        marker.color.g = 0.4
        marker.color.b = 0.8
        marker.color.a = 1.0  # Solid color (no transparency)
        self.marker_pub.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    node = SimBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()