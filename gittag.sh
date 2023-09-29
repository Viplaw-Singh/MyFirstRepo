#!/bin/bash

# Define your environment variables or settings
ENV_NAME="production"
DEPLOY_COMMAND="./deploy.sh"  # Replace with your actual deployment command

# Check if the pushed reference is a tag
while read oldrev newrev refname; do
  if [[ $refname =~ ^refs/tags/ ]]; then
    TAG_NAME=${refname#refs/tags/}
    echo "Tag $TAG_NAME was pushed. Deploying to $ENV_NAME..."

    # Perform your deployment or environment setup actions here
    echo "Running deployment command: $DEPLOY_COMMAND"
    $DEPLOY_COMMAND

    # Add any additional actions you need
  fi
done

