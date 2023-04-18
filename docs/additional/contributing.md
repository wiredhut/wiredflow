# Contribution guide

This is an open-source library. That means you can also make changes, 
fix bugs, and suggest new features. To do most effectively, follow the 
guide we compiled just for you. 

Good luck!

## Check documentation

Please take a look at the "Common description" documentation section. 
It will help you understand what terms are used in the description and during the discussions,
and what components are used in the library.

It is worth carefully exploring the section [Architecture of wiredflow (for developers)](../common/architecture.md) if you would like to propose changes in the source code.
In this document you will find all the necessary explanations about the internal organization of the library. 
So, our advice is "Explore the architecture before starting source code modification". It will help integrate your 
developments more efficiently into the project and simplify the code review process for both you and the maintainers.

## Check issues and discussion

If you are already familiar with the architecture of the project, then it's time to check the [current issues
of the wiredflow](https://github.com/wiredhut/wiredflow/issues). 
If among the open issues there are those you would like to implement, then you can offer your candidacy in the comments.
If there is no functionality (or a bug that you discovered) among the open issues that you would like 
to see in the framework, create your own item in issues or in discussions. 

Once you've created an issue, you can wait for some of the maintainers to look at it and put their 
comments. Or, if you are confident enough, you can start implementing proposed fixes.

It's also worth checking the ["Discussion"](https://github.com/wiredhut/wiredflow/discussions) section. There 
may be a thread in which there was a discussion on a topic you interested about.

## Create a new branch and prepare Pull request (PR)

To make changes to the framework you will need to create a separate branch and go through a code review procedure. 
Note that you can suggest changes not only to the source code but also to the documentation, write posts about
library, etc. 

If you do not have write access to the repository, you need to: 

1. Make a fork of the repository: [Fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo) (skip this step if ypu already has write access)
2. Create separate branch (my-feature): `git checkout -b my-feature main`
3. Do some magic - implement your ideas
4. [Create Pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
5. Fix suggestions of project maintainers (or argue your position in a reasoned way) during review

Below are some recommendations for changes you will need to make to the code if 
you want to include the new stage implementation in wiredflow (very likely this is the change you want to make).

### Integrate new storage stage

### Integrate new send stage

### Integrate new connector

It is more ambitious and complicated task. 

## Enjoy results of your work!

And yes, this is an important section.
You did a great job. Even if your PR was not accepted (please don't get upset) - you still tried 
very hard, and we appreciate it!
