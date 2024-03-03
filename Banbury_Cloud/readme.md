# Banbury Cloud

## Introduction

This is a repository of all things Banbury Cloud. This will serve as a way for computers to talk to each other. This can be incredibly important, especially in the realm of AI. I would love to see this project go in a few different directions. This could be a modern solution for cloud services for both Retail and Enterprise level users. Of course, I also see this as an opportunity in AI. Potentially developing this into a platform that allows training and inference across all of your devices in the network. This could potentially limit the cost of spinning up a VM instance on AWS or Google Cloud in order to train machine learning models, by utilizing the power of all of your devices at the same time. 

## Structure

I built a little diagram to describe what I have in mind. We are able to collect a bunch of different pieces of data about our computers. If we actually collect this data over a period of time, we can eventually create accurate inferences of what the computer might be doing in the future through the use of Deep Learning techniques. Once we have some accurate inferences of what the computer might look like in the future, whether it is predicted to have an incredibly fast wifi speed or if its predicted to just be completely offline, we can make informed decisions on various tasks, such as where we want some of our files to be stored. 

For example, if I turn off a specific device every night at 5pm, Deep Learning would eventually be able to predict that this device would mostly likely be turned off at 5pm, and send all of its files to another device that is more likely to be on during that time.


<p align="center">
  <img src="https://github.com/Banbury-inc/Athena/blob/main/Banbury_Cloud/bcloud_structure.png" height="500" alt="Athena Structure"/>
</p>
<p align="center">  


## But why Electron? What's up with the relay server?

The biggest problem with this project is that I had to figure out a way to be able to access devices regardless of what wifi network they are on. There are a lot of complications with this, especially when there are a bunch of issues with port forwarding. I flirted with many different ideas such as using IPFS, but came across similar issues. I decided that the best option would be to create a relay server, and essentially have a web socket open. This completely eliminates the problem with port forwarding and creates a seamless solution for users to connect devices on separate networks. 

The reason why I chose electron is because I need software that is capable of performing tasks on the actual operating system. For example, downloading, uploading, and deleting files. This is difficult to do with a standard web app. By using a desktop app, we have a lot more control over what we can do with a users computer. 




i
