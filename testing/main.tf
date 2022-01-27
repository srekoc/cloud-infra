variable "vm_ips" {
    default = [
        [
            "10.81.7.33",
            "fe80::250:56ff:feb0:372e",
        ],
        [
            "10.81.7.34",
            "fe80::250:56ff:feb0:f76e",
        ],
        [
            "10.81.7.35",
            "fe80::250:56ff:feb0:37e9",
        ]
    ]
}

variable "vm_macs" {
    default = [
        [
            "fe80::250:56ff:feb0:372e",
        ],
        [
            "fe80::250:56ff:feb0:f76e",
        ],
        [
            "fe80::250:56ff:feb0:37e9",
        ]
    ]
}

resource "random_pet" "example" {
  for_each = var.vm_ips
}

#> concat(flatten([for s in var.vm_ips: s[0]]), flatten(var.vm_macs))
#[
#  "10.81.7.33",
#  "10.81.7.34",
#  "10.81.7.35",
#  "fe80::250:56ff:feb0:372e",
#  "fe80::250:56ff:feb0:f76e",
#  "fe80::250:56ff:feb0:37e9",
#]
