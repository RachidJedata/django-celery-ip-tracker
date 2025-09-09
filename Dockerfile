# Use the official Redis image as base
FROM redis:latest

# Expose the Redis port
EXPOSE 6379

# Command to run Redis server
CMD ["redis-server"]
