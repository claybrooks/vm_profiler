#!/bin/bash

memory=2

test_ssh() {
    ssh clay-kvm@kvm-$1 "echo hello"
}

vm_mem() {
    echo "virsh setmem ubuntu18.10-${1} ${2}G --config"
    virsh setmaxmem ubuntu18.10-$1 $2G --config
    virsh setmem ubuntu18.10-$1 $2G --config
}

vm_start() {
    virsh start ubuntu18.10-$1
}

vm_shutdown() {
    virsh shutdown ubuntu18.10-$1
}

vm_wait() {
    while ! timeout 0.2 ping -c 1 -n kvm-$1 &> /dev/null
    do
        echo "waiting for kvm-${1}"
    done
}

vm_clean_repo() {
    ssh -t clay-kvm@kvm-$1 "cd ~/Desktop/git/vm_profiler; sudo git merge --abort; sudo git stash; sudo git reset --hard origin/master; sudo git stash drop; sudo git pull" &
}

vm_run_test() {
    ssh -t -X clay-kvm@kvm-$1 "cd ~/Desktop/git/vm_profiler; sudo git pull; ./runMultiVMTests.bash kvm" &
}

vm_push_results() {
    sleep 1s
    ssh -t clay-kvm@kvm-$1 "cd ~/Desktop/git/vm_profiler; sudo git pull; sudo git add results/*; sudo git commit -m \"Adding multi VM results from clay-kvm:${1}\"; git push"
}

run () {
    
    for i in `seq 1 $1`;
    do
        vm_mem $i $memory
    done

    for i in `seq 1 $1`;
    do
        vm_start $i
    done

    for i in `seq 1 $1`;
    do
        vm_wait $i
    done

    sleep 10s

    for i in `seq 1 $1`;
    do
        vm_clean_repo $i
    done

    for i in `seq 1 $1`;
    do
        vm_run_test $i
    done

    wait

    for i in `seq 1 $1`;
    do
        vm_push_results $i
        sleep 1s
        vm_shutdown $i
    done
}

run $1