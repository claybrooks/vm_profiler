#!/bin/bash

memory=2

test_ssh() {
    ssh clay-virtualbox@vb-$1 "echo hello"
}

vm_start() {
    VBoxManage startvm ubuntu_$1 --type headless
}

vm_shutdown() {
    VBoxManage controlvm ubuntu_$1 poweroff --type headless
}

vm_wait() {
    while ! timeout 0.2 ping -c 1 -n vb-$1 &> /dev/null
    do
        echo "waiting for vb-${1}"
    done
}

vm_clean_repo() {
    ssh -t clay-virtualbox@vb-$1 "cd ~/Desktop/git/vm_profiler; sudo git merge --abort; sudo git stash; sudo git reset --hard origin/master; sudo git stash drop; sudo git pull" &
}

vm_run_test() {
    ssh -t -X clay-virtualbox@vb-$1 "cd ~/Desktop/git/vm_profiler; git pull; ./runMultiVMTests.bash vb $1 $2" &
}

vm_push_results() {
    sleep 1s
    ssh -t clay-virtualbox@vb-$1 "cd ~/Desktop/git/vm_profiler; sudo git pull; sudo git add results/*; sudo git commit -m \"Adding multi VM results from clay-virtualbox:${1}\"; git push"
}

run () {

    for i in `seq 1 $1`;
    do
        vm_start $i
    done

    for i in `seq 1 $1`;
    do
        vm_wait $i
    done

    sleep 5s

    #for i in `seq 1 $1`;
    #do
    #    vm_clean_repo $i
    #done

    for i in `seq 1 $1`;
    do
        vm_run_test $i $1
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