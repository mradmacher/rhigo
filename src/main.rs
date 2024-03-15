// https://www.rohde-schwarz.com/webhelp/smb100a_html_usermanual_1/Content/2e097e6397fa40bd.htm#d79403e12303

fn main() -> visa_rs::Result<()>{
    use std::ffi::CString;
    use std::io::{BufRead, BufReader, Read, Write};
    use visa_rs::prelude::*;
  
    // open default resource manager
    let rm: DefaultRM = DefaultRM::new()?;
  
    // expression to match resource name
    let expr = CString::new("?*").unwrap().into();
    //let expr = CString::new("TCPIP::rssmb100m101624::hislip0").unwrap().into();
    //let expr = CString::new("TCPIP::rssmb100m101624::instr").unwrap().into();
    //let expr = CString::new("tcpip::192.168.1.8::hislip0").unwrap().into();
  
    let mut result =  rm.find_res_list(&expr).unwrap();
    eprintln!("{}", result.find_next().unwrap().unwrap());
    // USB0::0x0AAD::0x0054::000000::INSTR
    // find the first resource matched
    let rsc = rm.find_res(&expr)?;
  
    // open a session to the resource, the session will be closed when rm is dropped
    let instr: Instrument = rm.open(&rsc, AccessMode::NO_LOCK, TIMEOUT_IMMEDIATE)?;
  
    // write message
    //(&instr).write_all(b"RST\n").map_err(io_to_vs_err)?;
    (&instr).write_all(b"*IDN?\n").map_err(io_to_vs_err)?;
    // read response
    // Rohde&Schwarz,SMB100M,1406.6000k42/101624,3.1.19.15-3.20.390.24
    let mut buf_reader = BufReader::new(&instr);
    let mut buf = String::new();
    buf_reader.read_line(&mut buf).map_err(io_to_vs_err)?;
    eprintln!("{}", buf);
    std::thread::sleep(std::time::Duration::from_millis(1000));

    println!("11111!");
    (&instr).write_all(b"SYST:ERR?\n").map_err(io_to_vs_err)?;
    let mut buf_reader = BufReader::new(&instr);
    let mut buf = String::new();
    buf_reader.read_line(&mut buf).map_err(io_to_vs_err)?;
    eprintln!("{}", buf);

    println!("22222!");
    (&instr).write_all(b"SYST:DISP:UPD 1\n").map_err(io_to_vs_err)?;
    (&instr).write_all(b"SYST:ERR?\n").map_err(io_to_vs_err)?;
    let mut buf_reader = BufReader::new(&instr);
    let mut buf = String::new();
    buf_reader.read_line(&mut buf).map_err(io_to_vs_err)?;
    eprintln!("{}", buf);

    println!("33333!");
    let _ = (&instr).write_all(b"OUTP 1\n").map_err(io_to_vs_err);

    (&instr).write_all(b"SYST:ERR?\n").map_err(io_to_vs_err)?;
    let mut buf_reader = BufReader::new(&instr);
    let mut buf = String::new();
    buf_reader.read_line(&mut buf).map_err(io_to_vs_err)?;
    eprintln!("{}", buf);
  
    println!("44444!");
    let _ = (&instr).write_all(b"FREQ 350KHz\n").map_err(io_to_vs_err);
    //std::thread::sleep(std::time::Duration::from_millis(3000));

    (&instr).write_all(b"SYST:ERR?\n").map_err(io_to_vs_err)?;
    let mut buf_reader = BufReader::new(&instr);
    let mut buf = String::new();
    buf_reader.read_line(&mut buf).map_err(io_to_vs_err)?;
    eprintln!("{}", buf);

    println!("55555!");
    let _ = (&instr).write_all(b"SOUR:POW:LEV:IMM:AMPL 9\n").map_err(io_to_vs_err);
    //std::thread::sleep(std::time::Duration::from_millis(3000));

    (&instr).write_all(b"SYST:ERR?\n").map_err(io_to_vs_err)?;
    let mut buf_reader = BufReader::new(&instr);
    let mut buf = String::new();
    buf_reader.read_line(&mut buf).map_err(io_to_vs_err)?;
    eprintln!("{}", buf);
    Ok(())
  }