# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.require_version ">= 2.3.0"
#TODO: this is a very old vagrant file from my salt series several years ago, needs some TLC...

#ANSIBLE_VERSION = ENV['ANSIBLE_VERSION'] || '3000.3'

# Supported distributions/versions

BOXES = {
        'centos'   =>  {
          '6' => 'bento/centos-6.8',
          '7' => 'bento/centos-7.8',
          '8' => 'almalinux/8',
          'default' => '8'
        },
        'ubuntu'   =>  {
          '1804' => 'bento/ubuntu-18.04',
          '2004' => 'bento/ubuntu-20.04',
          'default' => '2004'
        },
        'windows'  =>  {
          '2012' => 'devopsgroup-io/windows_server-2012r2-standard-amd64-nocm',
          'default' => '2012'
        },
        'rhel'  =>  {
          '7' => 'generic/rhel7',
          '8' => 'generic/rhel8',
          'default' => '8'
        }
  }

# Default distribution is CentOS version 7
# Use LINUX_DISTRO and LINUX_VERSION to override

LINUX_DISTRO = ENV['LINUX_DISTRO'] || ENV['LINUX_DISTRIBUTION'] || 'centos'
LINUX_VERSION = ENV['LINUX_VERSION'] || BOXES[LINUX_DISTRO]['default']

if not BOXES[LINUX_DISTRO].has_key?(LINUX_VERSION)
  puts "Invalid version '#{LINUX_VERSION}' for #{LINUX_DISTRO}!\n\nValid versions: #{BOXES[LINUX_DISTRO].keys}"
  Kernel.exit(1)
end

LINUX_BOX = BOXES[LINUX_DISTRO][LINUX_VERSION]
puts "Chose Linux image #{LINUX_BOX} from args LINUX_DISTRO=#{LINUX_DISTRO} LINUX_VERSION=#{LINUX_VERSION}"


# Default Windows distribution is 2012r2 standard
# Use WINDOWS_VERSION or WINDOWS_BOX to override #TODO: add win 2016 version when its available
WINDOWS_VERSION = ENV['WINDOWS_VERSION'] || BOXES['windows']['default']
WINDOWS_BOX = BOXES['windows'][WINDOWS_VERSION]

puts "Chose Windows image #{WINDOWS_BOX} from args WINDOWS_BOX=#{WINDOWS_BOX} WINDOWS_VERSION=#{WINDOWS_VERSION}"

LINUX_MINION_COUNT = ENV['LINUX_MINION_COUNT'] || '1'
LINUX_BOX_RAM = ENV['LINUX_BOX_RAM'] || '512'


LINUX_SCRIPT = <<EOF
echo 'nothing here right now'
EOF

Vagrant.configure('2') do |config|
  if Vagrant.has_plugin?("vagrant-cachier")
 config.cache.scope = :box
  end
  if Vagrant.has_plugin?("vagrant-hostmanager")
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = false
  config.hostmanager.manage_guest = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true
  end
  config.vm.define 'primary' do |primary|
    primary.vm.provider "virtualbox" do |v|
      v.memory = LINUX_BOX_RAM.to_i
      v.linked_clone = true
 end
 primary.vm.box = LINUX_BOX
 primary.vm.hostname = 'primary'
 primary.vm.network 'private_network', ip: '192.168.56.4'
 primary.vm.synced_folder './dist', '/srv'
 #primary.vm.provision 'shell', inline: LINUX_SCRIPT
 primary.vm.provision "ansible_local" do |ansible|
  ansible.verbose = "v"
  ansible.playbook = "playbook.yml"
 end
  end
  (1..LINUX_MINION_COUNT.to_i).each do |i|
 config.vm.define "linux-#{i}" do |linux|
 linux.vm.provider "virtualbox" do |v|
   v.customize ['modifyvm', :id, '--natnet1', "10.#{i}.2.0/24"]
   v.memory = LINUX_BOX_RAM.to_i
   v.linked_clone = true
 end
 linux.vm.hostname = "linux-#{i}"
 linux.vm.box = LINUX_BOX
 linux.vm.network 'private_network', ip: "192.168.56.#{i+4}"
 #linux.vm.provision 'shell', inline: LINUX_SCRIPT
 linux.vm.provision "ansible" do |ansible|
  ansible.verbose = "v"
  ansible.playbook = "playbook.yml"
 end
 end
 end
  config.vm.define 'windows', autostart: false do |windows|
 windows.vm.provider "virtualbox" do |v|
   v.linked_clone = true
 end
end
end
