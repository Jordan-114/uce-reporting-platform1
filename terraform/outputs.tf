output "alb_dns" {
  description = "DNS del Load Balancer (API Gateway)"
  value       = aws_lb.alb.dns_name
}

output "ec2_public_ip" {
  description = "IP publica de la instancia EC2"
  value       = aws_instance.microservices.public_ip
}
