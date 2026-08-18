# EC2 Auto Scaling Configuration

resource "aws_launch_template" "app" {
name_prefix   = "three-tier-app-"
image_id      = "ami-xxxxxxxxxxxxxxxxx"
instance_type = "t3.micro"

user_data = base64encode(<<-EOF
#!/bin/bash
echo "Application Server" > /var/www/html/index.html
EOF
)

tag_specifications {
resource_type = "instance"


tags = {
  Name = "three-tier-app-server"
}


}
}

resource "aws_autoscaling_group" "app" {
min_size         = 2
max_size         = 4
desired_capacity = 2

launch_template {
id      = aws_launch_template.app.id
version = "$Latest"
}

vpc_zone_identifier = [
aws_subnet.private.id
]

health_check_type = "EC2"

tag {
key                 = "Name"
value               = "app-autoscaling"
propagate_at_launch = true
}
}
