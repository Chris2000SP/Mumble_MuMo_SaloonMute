#!/usr/bin/env python
# -*- coding utf-8

# Copyright (C) 2018 Chris2000SP <chris2000sp@googlemail.com>
# Copyright (C) 2013 Stefan Hacker <dd0t@users.sourceforge.net>
# All rights reserved

#
# saloonmute.py
#

## Global Variable ##
varMuteAktive=False
varUserSessionToMute=[]
varUserChannelToMute=[]
otherusers=[]

from mumo_module import (commaSeperatedIntegers,
			 MumoModule)
#from threading import Timer
import re
import cgi

class saloonmute(MumoModule):
	default_config = {'saloonmute':(
                ('servers', commaSeperatedIntegers, []),
        ),
        }

	def __init__(self, name, manager, configuration = None):
		MumoModule.__init__(self, name, manager, configuration)
		self.murmur = manager.getMurmurModule()
		self.action_info = manager.getUniqueAction()
                self.action_muteAktive = manager.getUniqueAction()
		self.watchdog = None

	def connected(self):
		manager = self.manager()
		log = self.log()
		log.debug("Register for Server callbacks")

		servers = self.cfg().saloonmute.servers
		if not servers:
			servers = manager.SERVERS_ALL

		manager.subscribeServerCallbacks(self, servers)

                try:
                        meta = manager.getMeta();
                        connServers = meta.getBootedServers();

                        userCount = 0
                        for serv in connServers:
                                userlist = serv.getUsers()
                                for user in userlist:
                                        #otherusers.append(userlist[user].name)
                                        entry = "%i-%s" % (serv.id(), userlist[user].name)
                                        log.debug("User chan: %s - Server: %i - %s", userlist[user].name, serv.id(), entry)
                                        userCount = userCount + 1
                        log.debug("Successfully took snapshot of user positions into memory for %i" % userCount)
                except:
                        log.debug("Could not load user data into memory. Will track moving forward.")

	def disconnected(self): pass

	def isTalking(self, server, action, user, target):
		assert action == self.action_info
		self.log().info(user.name + " wants info on " + str(user));
		#server.sendMessage(user.session,
                #        "<small><pre>" + cgi.escape(str(user)) + "</pre></small>")
                #while len(varUserSessionToMute) < 0:
                        #userlist
                        #if varMuteAktive:
                                # do something
                        

        def muteAktive(self, server, action, user, target):
                assert action == self.action_muteAktive
                self.log().info(user.name +
                                " will surpressed if some one talks in Channel");
                varUserSessionToMute.append(user.session)
                varUserChannelToMute.append(user.channel)
                
	def userConnected(self, server, user, context = None):

		self.log().info("Adding menu entries for " + user.name)

		manager = self.manager()
		manager.addContextMenuEntry(
			server,
			user,
			self.action_info,
			"Info",
			self.isTalking,
			self.murmur.ContextUser
		)

                manager.addContextMenuEntry(
                        server,
                        user,
                        self.action_muteAktive,
                        "Saloon Mute on Speak",
                        self.muteAktive,
                        self.murmur.ContextUser
                )
                
	def userDisconnected(self, server, state, context = None): pass
	def userStateChanged(self, server, state, context = None): pass
	def userTextMessage(self, server, user, message, current = None): pass
	def channelCreated(self, server, state, context = None): pass
	def channelRemoved(self, server, state, context = None): pass
	def channelStateChanged(self, server, state, context = None): pass
