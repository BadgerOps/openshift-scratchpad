# openshift-scratchpad

The given install-config.yaml is invalid, chatgpt decided you could just slap `ntpServers` in and call it a day. Lol.

Doing some reading into the [Manifest customization](https://docs.openshift.com/container-platform/4.12/installing/installing_bare_metal_ipi/ipi-install-installation-workflow.html#configuring-ntp-for-disconnected-clusters_ipi-install-installation-workflow) section, we can see an example of using butane to create custom manifests to embed.

we throw any custom files into a `manifests` directory and the installer will pick them up.

Example:

```bash
butane butane-master-ntp.bu -o manifests/98-master-chrony.yaml
``````