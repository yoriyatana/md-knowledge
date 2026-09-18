# capture the ttrace output

Please find the answers.

 

1/. Once we capture the ttrace output, will the result be saved in the FPC? And we can check it by executing the command "show ttrace" in the PFE mode, right?

[JTAC] Yes, this command will show the number of ttrace client was executed.

NGMPC0(jtac-mx480-r2006-re0 vty)# show ttrace                               

 Idx PFE ASIC PPE Ctx Zn   Pending     IDX/Steps/Total  FLAG  CURR_PC  Label

  0   0    0   1   1  19              757/  756/ 1000  SAVE  0x02b7   send_pkt_terminate_if_all_done_2

  1   0    0   0  20  30              757/  756/ 1000  SAVE  0x02b7   send_pkt_terminate_if_all_done_2

  2   0    0   0  10  30              757/  756/ 1000  SAVE  0x02b7   send_pkt_terminate_if_all_done_2

<..>

31   0    0   1  16  22              757/  756/ 1000  SAVE  0x02b7   send_pkt_terminate_if_all_done_2

 

2/. How many the number of ttrace that limit on MPC?

[JTAC] The limit is 32(0-31) clients. I noticed fpc crash when I ran ttrace after this limit in a lab device.

 

3/. As you said it hit the number limitation of ttrace so it caused FPC to raise the major alarm "Major alarm set, FPC 0 Major Errors - Lkup Error code: 0x40008". Could you please explain the logic on this point?

[JTAC] I will check this and get back once I have more details on this.

 

4/. Is there any potential risk if we execute "bringup ttrace <idx number> delete <<<<< delete all the historic ttrace."?

[JTAC] No, this will delete the ttrace clients and should not cause any impact.

 

5/. From what you stated, I understand that before performing capture the ttrace output, we need to check the historic ttraces by exceting "show ttrace". If there was a file on the output of this CLI, we need to delete them first and then performing capture the ttrace output. Please correct me if I'm wrong.

[JTAC] Yes, this is correct.
