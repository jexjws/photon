#!/bin/bash

set -x

if [ "$#" -lt 0 ]; then
	echo "Script to create new Photon OSTree repo inside a docker container."
	echo "Usage: $0 "
	exit -1
fi

PROGRAM=$0
SRCROOT=$1
STAGE_DIR=$2
PHOTON_DOCKER_IMAGE=$3

cat > ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh << EOF
#!/bin/bash

ROOT=$1

sed -i 's#https://dl.bintray.com/vmware#https://packages.vmware.com/photon/\$releasever#g' /etc/yum.repos.d/*.repo
tdnf install -y rpm
mkdir -p ${ROOT}/srv/rpm-ostree
ostree --repo=${ROOT}/srv/rpm-ostree/repo init --mode=archive-z2
rpm-ostree compose tree --repo=${ROOT}/srv/rpm-ostree/repo photon-base.json
EOF

chmod +x ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh

cp ${SRCROOT}/support/image-builder/ostree-tools/photon-ostree.repo ${SRCROOT}/support/image-builder/ostree-tools/photon-ostree.repo.bak
echo "baseurl=file:///RPMS" >> ${SRCROOT}/support/image-builder/ostree-tools/photon-ostree.repo

rm -rf ${STAGE_DIR}/ostree-repo
mkdir -p ${STAGE_DIR}/ostree-repo

sudo docker run --privileged -v ${SRCROOT}:/photon -v ${STAGE_DIR}/RPMS:/RPMS -v ${STAGE_DIR}/ostree-repo:/srv/rpm-ostree -w="/photon/support/image-builder/ostree-tools/" ${PHOTON_DOCKER_IMAGE} ./mk-ostree-server.sh /

REPODIR=${STAGE_DIR}/ostree-repo/repo
if [ -d "$REPODIR" ]; then
  tar -zcf ${STAGE_DIR}/ostree-repo.tar.gz -C ${REPODIR} .
fi

# Restore file
mv -f ${SRCROOT}/support/image-builder/ostree-tools/photon-ostree.repo.bak ${SRCROOT}/support/image-builder/ostree-tools/photon-ostree.repo
sudo rm ${SRCROOT}/support/image-builder/ostree-tools/mk-ostree-server.sh
sudo rm -rf ${STAGE_DIR}/ostree-repo