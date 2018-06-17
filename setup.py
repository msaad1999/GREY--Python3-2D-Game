import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

import cx_Freeze

executables = [cx_Freeze.Executable("GREY.pyw")]

cx_Freeze.setup(
    name="GREY",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":['bullet2.png','machinegun.png','icon.jpg','bg1.png','bg2.png','intro.png','me.png','grey.png','start.wav','gameMusic.wav','gameeasy.wav','gamehard.wav','gameover.wav','haha.wav','expl.wav','thud.wav','powerup.wav','gunshot.wav','bomb.wav','shotgun.wav','cloud (1).png','cloud (2).png','cloud (3).png','cloud (4).png','Picture1.png','Picture2.png','Picture3.png','Picture4.png','Picture5.png','Picture6.png','Picture7.png','Picture8.png','Picture9.png','regularExplosion00.png','regularExplosion01.png','regularExplosion02.png','regularExplosion03.png','regularExplosion04.png','regularExplosion05.png','regularExplosion06.png','regularExplosion07.png','regularExplosion08.png','e_jet.png','snow.png','jet.png','bullet.png','ebullet.png','pauseimg.png','paused.png','menu.jpg','menu2.jpg','credits.png','guide.png','died.png','skull.jpg','ember.png','upgraded.png','jet2.png','jet3.png','jet4.png','e_jet2.png','e_jet3.png','vcruntime140.dll']}},
    executables = executables

    ) 
