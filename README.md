# quinceleaf / csa-member-management

## Problem

**Community Supported Agriculture** is a business model that has been growing in popularity over the past several decades, as local farmers have sought ways of remaining economically viable and food-conscious consumers have sought to support local businesses.

In its most common form, with a CSA a farm offers members weekly or bi-weekly deliveries of a basket of the farm's produce. In return, members pay a membership fee prior to the harvest season - either as a one-time payment or staggered - which helps provide the farm with cash flow.

It can be an attractive alternative to or supplement alongside participating in regional farmers' markets.

However, the challenges of connecting with interested consumers, handling subscription payments and planning & scheduling deliveries can be substantial.

There are a handful of software-as-a-service (SaaS) offerings on the market that attempt to provide farmers and members with solutions to these challenges. While these platforms provide useful solutions, there is a lack of truly affordable options:

- some charge as much as $600/month ($7,200/annually)
- others charge the farm a percentage of the subscriptions managed


## Solution

This project represents an attempt to quickly produce a robust alternative to existing platforms. Development will be undertaken in a series of short sprints, building out different aspects.


## Planned Tech Stack

This stack is subject to change, but initially my plan is to use:

- [Django](https://www.djangoproject.com/) for the backend & business logic
- [Django REST Framework](https://www.django-rest-framework.org/) for the API
- [PostgreSQL](https://www.postgresql.org) for the database
- [React.js](https://reactjs.org) and [Tailwind CSS](https://tailwindcss.com) for the frontend
- [Mapbox](https://www.mapbox.com) for mapping and route planning


## Resources

- LocalHarvest, ["Community Supported Agriculture"](https://www.localharvest.org/csa/)
- Tom Preston-Werner, ["Readme Driven Development"](https://tom.preston-werner.com/2010/08/23/readme-driven-development.html)